# Slideshow Creation Guide

## Overview

This guide explains how to create a dynamic, responsive HTML slideshow that displays exercise content with background images. The slideshow generates **2 slides per exercise** (title slide + content slide), resulting in **N×2 total slides** where N is the number of exercises.

## What Was Created

A single, self-contained HTML file (`slideshow.html`) that:
- Displays exercises in sequence from `exercises_selection.md`
- Uses images from the `assets/` directory (one per exercise)
- Shows title slides with full background images
- Shows content slides with semi-transparent backgrounds and clear text
- Includes navigation controls (buttons, keyboard, touch/swipe)
- Is fully responsive for mobile, tablet, and desktop

## Structure Requirements

Before creating the slideshow, ensure you have:

1. **Exercise Sequence**: A document (like `exercises_selection.md`) that lists exercises in order
2. **Exercise Folders**: Each exercise in its own folder under `exercises/`
3. **Exercise Content**: Each folder contains `exercise_starter.md` with the exercise text
4. **Assets Directory**: Contains images matching exercise names (e.g., `intro_python.jpg`, `etl_merger.jpg`)

## Step-by-Step Process

### Step 1: Identify Exercise Sequence

Review `exercises_selection.md` to determine the order of exercises. The sequence should match:
- The order in the document
- The image filenames in `assets/`
- The folder names in `exercises/`

**Example sequence:**
1. Intro: Hello World → `intro_python.jpg`
2. ETL 1: The Great Merger → `etl_merger.jpg`
3. ETL 2: The Detective → `etl_detective.jpg`
4. ... and so on

### Step 2: Extract Exercise Data

For each exercise, collect:
- **Exercise Number/Identifier**: (e.g., "Intro", "ETL 1", "Viz 2")
- **Exercise Title**: The main title from `exercise_starter.md`
- **Image Path**: Relative path to image in `assets/` (e.g., `assets/intro_python.jpg`)
- **Exercise Content**: Full text from `exercise_starter.md`

### Step 3: Create HTML Structure

Create a new HTML file with:

#### Basic HTML Structure
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Workshop Exercises Slideshow</title>
    <style>
        /* CSS styles go here */
    </style>
</head>
<body>
    <div class="slideshow-container" id="slideshow"></div>
    <button class="nav-button prev" onclick="changeSlide(-1)">‹</button>
    <button class="nav-button next" onclick="changeSlide(1)">›</button>
    <div class="slide-counter" id="counter">1 / N</div>
    <script>
        /* JavaScript goes here */
    </script>
</body>
</html>
```

### Step 4: Define Exercise Data Array

Create a JavaScript array with exercise objects:

```javascript
const exercises = [
    {
        number: "Intro",
        title: "Hello World - The First Flight",
        image: "assets/intro_python.jpg",
        content: `# Exercise Title\n\n## The Goal\n\nExercise description...`
    },
    {
        number: "ETL 1",
        title: "The Great Merger",
        image: "assets/etl_merger.jpg",
        content: `# Exercise: The Great Merger\n\n...`
    },
    // ... more exercises
];
```

**Key Points:**
- Use template literals (backticks) for multi-line content
- Keep image paths relative to HTML file location
- Include full markdown content from `exercise_starter.md`

### Step 5: Create Slide Generation Function

Generate two slides per exercise:

```javascript
function generateSlides() {
    exercises.forEach((exercise, index) => {
        // Slide 1: Title slide
        const titleSlide = document.createElement('div');
        titleSlide.className = 'slide slide-title';
        titleSlide.style.backgroundImage = `url('${exercise.image}')`;
        titleSlide.innerHTML = `
            <div class="content">
                <div class="exercise-number">${exercise.number}</div>
                <h1>${exercise.title}</h1>
            </div>
        `;
        slideshow.appendChild(titleSlide);

        // Slide 2: Content slide
        const contentSlide = document.createElement('div');
        contentSlide.className = 'slide slide-content';
        contentSlide.style.backgroundImage = `url('${exercise.image}')`;
        contentSlide.innerHTML = `
            <div class="content">
                ${markdownToHtml(exercise.content)}
            </div>
        `;
        slideshow.appendChild(contentSlide);
    });
}
```

### Step 6: Implement Markdown Parser

Create a function to convert markdown to HTML:

```javascript
function markdownToHtml(text) {
    const lines = text.split('\n');
    let result = [];
    let inList = false;
    
    for (let i = 0; i < lines.length; i++) {
        let line = lines[i].trim();
        
        if (!line) {
            if (inList) {
                result.push('</ul>');
                inList = false;
            }
            continue;
        }
        
        // Process headers (#, ##, ###)
        if (line.startsWith('### ')) {
            if (inList) {
                result.push('</ul>');
                inList = false;
            }
            result.push('<h3>' + processInlineMarkdown(line.substring(4)) + '</h3>');
        } else if (line.startsWith('## ')) {
            if (inList) {
                result.push('</ul>');
                inList = false;
            }
            result.push('<h3>' + processInlineMarkdown(line.substring(3)) + '</h3>');
        } else if (line.startsWith('# ')) {
            if (inList) {
                result.push('</ul>');
                inList = false;
            }
            result.push('<h2>' + processInlineMarkdown(line.substring(2)) + '</h2>');
        }
        // Process list items
        else if (/^[\d*\-]\.?\s+/.test(line)) {
            if (!inList) {
                result.push('<ul>');
                inList = true;
            }
            const listContent = line.replace(/^[\d*\-]\.?\s+/, '');
            result.push('<li>' + processInlineMarkdown(listContent) + '</li>');
        }
        // Process horizontal rules
        else if (line === '---') {
            if (inList) {
                result.push('</ul>');
                inList = false;
            }
            result.push('<hr>');
        }
        // Process regular paragraphs
        else {
            if (inList) {
                result.push('</ul>');
                inList = false;
            }
            result.push('<p>' + processInlineMarkdown(line) + '</p>');
        }
    }
    
    if (inList) {
        result.push('</ul>');
    }
    
    return result.join('\n');
}

function processInlineMarkdown(text) {
    return text
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.+?)\*/g, '<em>$1</em>')
        .replace(/`(.+?)`/g, '<code>$1</code>');
}
```

### Step 7: Implement Navigation

Add slide navigation functions:

```javascript
let currentSlide = 0;

function changeSlide(direction) {
    const slides = slideshow.querySelectorAll('.slide');
    slides[currentSlide].classList.remove('active');
    
    currentSlide += direction;
    
    if (currentSlide < 0) {
        currentSlide = slides.length - 1;
    } else if (currentSlide >= slides.length) {
        currentSlide = 0;
    }
    
    slides[currentSlide].classList.add('active');
    updateCounter();
}

function updateCounter() {
    const slides = slideshow.querySelectorAll('.slide');
    counter.textContent = `${currentSlide + 1} / ${slides.length}`;
}

// Keyboard navigation
document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowLeft') changeSlide(-1);
    if (e.key === 'ArrowRight') changeSlide(1);
});

// Touch/swipe support
let touchStartX = 0;
let touchEndX = 0;

slideshow.addEventListener('touchstart', (e) => {
    touchStartX = e.changedTouches[0].screenX;
});

slideshow.addEventListener('touchend', (e) => {
    touchEndX = e.changedTouches[0].screenX;
    if (touchEndX < touchStartX - 50) changeSlide(1);
    if (touchEndX > touchStartX + 50) changeSlide(-1);
});
```

### Step 8: Style the Slideshow

Add CSS for:

#### Slide Container
- Full viewport size (`100vw × 100vh`)
- Absolute positioning for slides
- Opacity transitions for fade effects

#### Title Slides
- Full background image (`background-size: cover`)
- Dark overlay for text readability
- Centered content with backdrop blur
- Large, bold title text

#### Content Slides
- Semi-transparent background (`rgba(0, 0, 0, 0.5)`)
- White content box with high opacity (`rgba(255, 255, 255, 0.95)`)
- Scrollable content area
- Responsive typography using `clamp()`

#### Navigation
- Fixed position buttons
- Circular design with hover effects
- Slide counter at bottom

## Key CSS Features

### Responsive Typography
```css
font-size: clamp(1rem, 1.8vw, 1.3rem);
```
Uses `clamp()` to scale text between minimum and maximum sizes based on viewport width.

### Backdrop Filter
```css
backdrop-filter: blur(10px);
```
Creates a frosted glass effect for better text readability over images.

### Smooth Transitions
```css
transition: opacity 0.8s ease-in-out;
```
Provides smooth fade transitions between slides.

## Customization Options

### Change Colors
Modify CSS variables or color values:
- Title slide overlay: `rgba(0, 0, 0, 0.4)`
- Content box background: `rgba(255, 255, 255, 0.95)`
- Accent color: `#64b5f6` (blue)

### Adjust Image Opacity
For content slides, change background overlay:
```css
.slide-content {
    background-color: rgba(0, 0, 0, 0.5); /* Increase for darker, decrease for lighter */
}
```

### Modify Transition Speed
```css
.slide {
    transition: opacity 0.8s ease-in-out; /* Change 0.8s to desired duration */
}
```

### Change Slide Layout
Modify content positioning:
- Title slides: `align-items: center; justify-content: center;`
- Content slides: Adjust padding and max-width for different layouts

## Testing Checklist

- [ ] All exercises appear in correct sequence
- [ ] Images load correctly (check paths)
- [ ] Title slides show correct titles
- [ ] Content slides display markdown correctly
- [ ] Navigation works (buttons, keyboard, touch)
- [ ] Slide counter updates correctly
- [ ] Responsive on mobile devices
- [ ] Text is readable on all slide types
- [ ] Transitions are smooth

## Troubleshooting

### Images Not Loading
- Check image paths are relative to HTML file location
- Verify image filenames match exactly (case-sensitive)
- Ensure images exist in `assets/` directory

### Markdown Not Rendering
- Check markdown syntax in exercise content
- Verify `markdownToHtml()` function handles all markdown features used
- Test with simpler markdown first

### Navigation Not Working
- Check JavaScript console for errors
- Verify `currentSlide` variable is initialized
- Ensure slides have correct classes (`slide`, `active`)

### Text Not Readable
- Adjust background overlay opacity
- Increase content box opacity
- Modify text colors for better contrast
- Check backdrop-filter browser support

## Future Enhancements

Potential improvements:
1. **Auto-play mode**: Automatically advance slides
2. **Progress bar**: Visual progress indicator
3. **Slide thumbnails**: Mini navigation panel
4. **Fullscreen mode**: Toggle fullscreen presentation
5. **Export to PDF**: Generate PDF version
6. **Presenter notes**: Add hidden notes for presenter
7. **Animation effects**: Add slide-in animations
8. **Theme switching**: Light/dark mode toggle

## Summary

The slideshow creation process involves:
1. **Data Collection**: Extract exercise sequence, titles, images, and content
2. **HTML Structure**: Create container, navigation, and counter elements
3. **JavaScript Logic**: Generate slides dynamically, parse markdown, handle navigation
4. **CSS Styling**: Design responsive, readable slides with smooth transitions
5. **Testing**: Verify all features work across devices

The result is a self-contained, portable HTML file that can be opened in any modern web browser without additional dependencies.
