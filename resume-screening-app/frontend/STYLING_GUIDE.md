# Resume Screening App - Styling Guide

This guide covers the comprehensive CSS utilities and styling patterns available in the Resume Screening App frontend.

## Table of Contents
- [Color System](#color-system)
- [Glassmorphism Effects](#glassmorphism-effects)
- [Button Styles](#button-styles)
- [Card Components](#card-components)
- [Input Fields](#input-fields)
- [Animations](#animations)
- [Utility Classes](#utility-classes)
- [Responsive Design](#responsive-design)
- [Best Practices](#best-practices)

## Color System

### Primary Colors
- **Purple Gradient**: `from-purple-400 to-pink-400`
- **Blue Gradient**: `from-blue-400 to-cyan-400`
- **Accent Gradient**: `from-orange-400 to-red-400`

### Background Gradients
```css
.gradient-bg-primary    /* Purple to blue to indigo */
.gradient-bg-secondary  /* Slate to gray to zinc */
.gradient-bg-accent     /* Pink to rose to red */
```

### Text Gradients
```css
.gradient-text-primary    /* Purple to pink text */
.gradient-text-secondary  /* Blue to cyan text */
.gradient-text-accent     /* Orange to red text */
```

## Glassmorphism Effects

### Basic Glassmorphism
```css
.glassmorphism        /* Standard glass effect */
.glassmorphism-light  /* Lighter glass effect */
.glassmorphism-dark   /* Darker glass effect */
.glassmorphism-ultra  /* Ultra blur effect */
```

### Specialized Components
```css
.glassmorphism-card   /* Card with glass effect */
.glassmorphism-nav    /* Navigation glass effect */
```

## Button Styles

### Gradient Buttons
```jsx
<button className="btn-gradient">Primary Button</button>
<button className="btn-outline-gradient">Outline Button</button>
<button className="btn-ghost-gradient">Ghost Button</button>
```

### Standard Buttons
```jsx
<button className="btn-primary">Primary</button>
<button className="btn-secondary">Secondary</button>
```

## Card Components

### Card Variations
```css
.card          /* Basic card with glass effect */
.card-hover    /* Card with hover effects */
.card-stats    /* Statistics card */
.card-feature  /* Feature highlight card */
```

### Usage Example
```jsx
<div className="card-hover">
  <h3>Card Title</h3>
  <p>Card content with glass effect</p>
</div>
```

## Input Fields

### Enhanced Inputs
```css
.input-field     /* Basic input */
.input-enhanced  /* Enhanced input with glass effect */
.input-search    /* Search input with special styling */
```

### Usage Example
```jsx
<input 
  type="text" 
  className="input-enhanced" 
  placeholder="Enter text..."
/>
```

## Animations

### Entrance Animations
```css
.animate-fade-in       /* Fade in from bottom */
.animate-fade-up       /* Fade in from top */
.animate-fade-down     /* Fade in from bottom */
.animate-slide-in-left /* Slide in from left */
.animate-slide-in-right /* Slide in from right */
```

### Interactive Animations
```css
.animate-bounce-gentle  /* Gentle bouncing effect */
.animate-pulse-glow     /* Pulsing glow effect */
.animate-float          /* Floating animation */
```

### Usage Example
```jsx
<div className="animate-fade-in">
  Content that fades in on load
</div>
```

## Utility Classes

### Text Effects
```css
.text-shadow      /* Small text shadow */
.text-shadow-lg   /* Large text shadow */
.text-shadow-xl   /* Extra large text shadow */
```

### Layout Utilities
```css
.hover-lift       /* Lift effect on hover */
.gradient-border  /* Gradient border */
.gradient-mask    /* Gradient mask for fading */
```

### Loading States
```css
.loading-shimmer  /* Shimmer loading effect */
.spinner          /* Loading spinner */
```

### Badges
```css
.badge-primary    /* Purple badge */
.badge-secondary  /* Blue badge */
.badge-accent     /* Pink badge */
.badge-success    /* Green badge */
.badge-warning    /* Yellow badge */
.badge-error      /* Red badge */
```

### Notifications
```css
.notification         /* Base notification */
.notification-success /* Success notification */
.notification-error   /* Error notification */
.notification-warning /* Warning notification */
.notification-info    /* Info notification */
```

## Responsive Design

### Mobile Utilities
```css
.mobile-glass  /* Glass effect optimized for mobile */
.mobile-nav    /* Mobile navigation styling */
```

### Responsive Breakpoints
Use Tailwind's built-in breakpoints:
- `sm`: 640px
- `md`: 768px
- `lg`: 1024px
- `xl`: 1280px
- `2xl`: 1536px

## Best Practices

### 1. Consistent Spacing
Use Tailwind's spacing scale for consistent margins and padding.

### 2. Color Harmony
Stick to the defined color gradients and avoid introducing new colors without updating the design system.

### 3. Performance Considerations
- Use `will-change` property sparingly
- Prefer CSS animations over JavaScript animations
- Optimize images and assets

### 4. Accessibility
- Ensure sufficient color contrast
- Use semantic HTML elements
- Provide proper focus states
- Support keyboard navigation

### 5. Browser Compatibility
All styles include vendor prefixes for cross-browser compatibility.

### 6. Dark Mode Support
The app includes dark mode variants for all components.

## Customization

### Adding New Styles
When adding new styles:
1. Add to the appropriate `@layer` in `index.css`
2. Include vendor prefixes for cross-browser support
3. Document the new utility in this guide
4. Test across different browsers and devices

### Theme Variables
Customize the theme by modifying CSS variables in the `:root` and `.dark` selectors.

## Examples

### Hero Section Example
```jsx
<section className="gradient-bg-primary min-h-screen flex items-center justify-center">
  <div className="glassmorphism-ultra p-12 text-center">
    <h1 className="gradient-text-primary text-4xl font-bold mb-4">
      Welcome to Resume Screening
    </h1>
    <p className="text-white/80 mb-8">
      Advanced AI-powered resume analysis
    </p>
    <button className="btn-gradient">
      Get Started
    </button>
  </div>
</section>
```

### Feature Card Example
```jsx
<div className="card-feature animate-fade-up">
  <div className="text-3xl mb-4">🚀</div>
  <h3 className="text-xl font-semibold mb-2">AI Analysis</h3>
  <p className="text-white/70">
    Advanced machine learning algorithms analyze resumes with precision.
  </p>
</div>
```

## Troubleshooting

### Common Issues
1. **Glass effects not working**: Ensure browser supports backdrop-filter
2. **Animations not firing**: Check if element is visible on page load
3. **Gradients not showing**: Verify browser support for CSS gradients

### Browser Support
- Chrome: Full support
- Firefox: Full support
- Safari: Full support with vendor prefixes
- Edge: Full support

---

*Last Updated: ${new Date().toLocaleDateString()}*
