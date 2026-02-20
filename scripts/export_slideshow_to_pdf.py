import os
import sys
import time
from playwright.sync_api import sync_playwright
from PIL import Image

def export_slideshow(html_path, output_pdf):
    # Ensure absolute path for local file
    abs_html_path = os.path.abspath(html_path)
    if not os.path.exists(abs_html_path):
        print(f"Error: File not found: {abs_html_path}")
        return

    print(f"Opening content from: {abs_html_path}")

    with sync_playwright() as p:
        # Launch browser (headless=True is default)
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1920, 'height': 1080})
        
        # Load the local HTML file
        url = f'file:///{abs_html_path}'
        page.goto(url)
        
        # Wait for the slideshow to initialize and slides to be created
        # The slideshow generates slides via JS (generateSlides function), so we wait for .slide
        try:
            page.wait_for_selector('.slide', timeout=10000)
        except Exception as e:
            print("Error: Slides did not load within timeout.")
            print(e)
            browser.close()
            return
        
        # Disable CSS transitions to speed up capture and avoid motion blur artifacts
        page.add_style_tag(content="""
            * { transition: none !important; }
            .slide { transition: none !important; opacity: 1 !important; display: none; }
            .slide.active { display: flex; }
        """)
        # Note: originally .slide has opacity:0 and .active has opacity:1.
        # We override this to ensure snap-visibility. 
        # Using display:none/flex might be safer to ensure no ghosting, 
        # but the original CSS uses opacity.
        # Let's stick to the original structure but kill the transition time.
        page.add_style_tag(content="""
            .slide { transition: none !important; }
        """)

        # Get total slides count
        total_slides = page.evaluate("document.querySelectorAll('.slide').length")
        print(f"Found {total_slides} slides.")
        
        screenshot_paths = []
        
        # Create a temp directory for screenshots if it doesn't exist
        temp_dir = os.path.join(os.path.dirname(abs_html_path), "tmp_pdf_slides")
        os.makedirs(temp_dir, exist_ok=True)

        for i in range(total_slides):
            # Manually activate the slide via JS to ensure we are exactly where we want to be
            page.evaluate(f"""
                (index) => {{
                    const slides = document.querySelectorAll('.slide');
                    // Remove active class from all
                    slides.forEach(s => s.classList.remove('active'));
                    // Add active class to target
                    slides[index].classList.add('active');
                    // Update global state if exists
                    if (typeof currentSlide !== 'undefined') currentSlide = index;
                    if (typeof updateCounter === 'function') updateCounter();
                }}
            """, i)
            
            # Allow a tiny render frame tick (though wait_for_timeout is usually discouraged, keeping it extremely short helps rendering catch up)
            # Since we disabled transitions, it should be instant.
            # However, background images might need a moment? 
            # They are likely preloaded or cached, but let's be safe.
            # page.wait_for_timeout(100) 
            
            # Take screenshot
            temp_path = os.path.join(temp_dir, f"slide_{i:03d}.png")
            page.screenshot(path=temp_path)
            screenshot_paths.append(temp_path)
            print(f"Captured slide {i+1}/{total_slides}")
            
        browser.close()
        
        print("Compiling PDF...")
        # Merge screenshots into PDF using Pillow
        if screenshot_paths:
            # Open first image
            first_image = Image.open(screenshot_paths[0]).convert('RGB')
            other_images = [Image.open(p).convert('RGB') for p in screenshot_paths[1:]]
            
            first_image.save(
                output_pdf, 
                "PDF", 
                resolution=100.0, 
                save_all=True, 
                append_images=other_images
            )
            print(f"Successfully created PDF: {output_pdf}")
            
            # Cleanup temp files
            print("Cleaning up temporary images...")
            for p in screenshot_paths:
                try:
                    os.remove(p)
                except:
                    pass
            try:
                os.rmdir(temp_dir)
            except:
                pass

if __name__ == "__main__":
    # Default to slideshow/slideshow.html in the parent/root directory relative to this script, or current dir
    default_target = os.path.join(os.path.dirname(__file__), "..", "slideshow", "slideshow.html")
    
    target_file = default_target
    if len(sys.argv) > 1:
        target_file = sys.argv[1]
        
    if not os.path.exists(target_file):
        # Try relative to CWD
        if os.path.exists(sys.argv[1]):
             target_file = sys.argv[1]
        else:
            print(f"Usage: python export_slideshow_to_pdf.py [path_to_html]")
            print(f"Default target not found: {default_target}")
            sys.exit(1)

    output_file = os.path.splitext(target_file)[0] + ".pdf"
    export_slideshow(target_file, output_file)
