---
name: Gym Buddy
colors:
  surface: '#f9f9ff'
  surface-dim: '#d3daef'
  surface-bright: '#f9f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f1f3ff'
  surface-container: '#e9edff'
  surface-container-high: '#e1e8fd'
  surface-container-highest: '#dce2f7'
  on-surface: '#141b2b'
  on-surface-variant: '#3e494a'
  inverse-surface: '#293040'
  inverse-on-surface: '#edf0ff'
  outline: '#6f797a'
  outline-variant: '#bec8ca'
  surface-tint: '#006972'
  primary: '#00535b'
  on-primary: '#ffffff'
  primary-container: '#006d77'
  on-primary-container: '#9becf7'
  inverse-primary: '#82d3de'
  secondary: '#236863'
  on-secondary: '#ffffff'
  secondary-container: '#a9ece5'
  on-secondary-container: '#286d67'
  tertiary: '#743b24'
  on-tertiary: '#ffffff'
  tertiary-container: '#915239'
  on-tertiary-container: '#ffd7c9'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#9ff0fb'
  primary-fixed-dim: '#82d3de'
  on-primary-fixed: '#001f23'
  on-primary-fixed-variant: '#004f56'
  secondary-fixed: '#acefe7'
  secondary-fixed-dim: '#90d3cb'
  on-secondary-fixed: '#00201e'
  on-secondary-fixed-variant: '#00504b'
  tertiary-fixed: '#ffdbce'
  tertiary-fixed-dim: '#ffb59a'
  on-tertiary-fixed: '#380d00'
  on-tertiary-fixed-variant: '#6f3720'
  background: '#f9f9ff'
  on-background: '#141b2b'
  surface-variant: '#dce2f7'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 28px
    fontWeight: '700'
    lineHeight: 36px
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.05em
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  base: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  gutter: 20px
  margin-mobile: 16px
  margin-desktop: 40px
---

## Brand & Style
The design system for this product centers on a **Clean Athletic Daylight** aesthetic. It is engineered for high-utility environments where clarity and performance are paramount. The visual language blends **Minimalism** with a **Corporate/Modern** structure to ensure the interface feels professional, reliable, and functional.

The target audience consists of students and fitness enthusiasts who require a tool that stays out of the way of their workout while providing highly legible data at a glance. The UI evokes a sense of freshness, focus, and energy through high-contrast elements and generous whitespace, mirroring the environment of a well-lit, modern training facility.

## Colors
The palette is rooted in a "Daylight" theme, prioritizing high legibility and a crisp feel.

*   **Primary (#006D77):** A deep teal used for primary actions, active states, and brand emphasis. It provides a sophisticated alternative to standard "gym blues."
*   **Neutral (#111827):** A near-black navy used for typography and high-contrast borders to ensure maximum readability.
*   **Surfaces:** The background utilizes a subtle off-white (#F9FAFB) to reduce eye strain, while cards and containers use pure white (#FFFFFF) to pop forward.
*   **Accents:** Secondary and tertiary tones (Teal-tint and Muted Coral) are reserved for data visualization and status indicators (e.g., progress bars, muscle group highlighting).

## Typography
This design system utilizes **Inter** exclusively to maintain a systematic, utilitarian, and modern appearance. 

*   **Headlines:** Bold weights with slight negative letter-spacing create a confident, impactful look for workout titles and screen headers.
*   **Labels:** Use medium or semi-bold weights with uppercase styling for secondary navigation and data category headers to distinguish them from body content.
*   **Scaling:** Large displays scale down on mobile to ensure the "Daylight" whitespace is preserved even on smaller viewports.

## Layout & Spacing
The layout follows a **Fluid Grid** model with strict 8px-based spacing increments. 

*   **Desktop:** 12-column grid with 20px gutters and large side margins to keep content centered and readable.
*   **Mobile:** 4-column grid with 16px margins.
*   **Rhythm:** Vertical rhythm is maintained through standard 16px (md) and 24px (lg) gaps between functional groups. Components should utilize internal padding of 16px to ensure touch targets are accessible during physical activity.

## Elevation & Depth
To maintain the "Clean" aesthetic, this design system avoids heavy drop shadows. Instead, it uses **Tonal Layers** and **Ambient Shadows**.

*   **Level 0 (Background):** #F9FAFB.
*   **Level 1 (Cards/Inputs):** Pure #FFFFFF with a 1px border (#E5E7EB) and a very soft, diffused shadow (0px 4px 12px rgba(0, 0, 0, 0.03)).
*   **Level 2 (Dropdowns/Modals):** Pure #FFFFFF with a more pronounced shadow (0px 10px 25px rgba(0, 0, 0, 0.08)) to indicate temporary interaction.
*   **Interaction:** Active elements should not "lift" excessively; instead, they should show depth through subtle color shifts or high-contrast borders.

## Shapes
The shape language is **Soft**, balancing professional structure with modern approachability. 

*   **Standard Elements:** Buttons and inputs use a 0.25rem (4px) radius to maintain a precise, engineered feel.
*   **Large Containers:** Cards and modals use a 0.5rem (8px) radius to soften the layout.
*   **Icons:** Use a consistent 2px stroke weight with slightly rounded joins to match the typography.

## Components
Consistent styling for the core gym-tracking experience:

*   **Buttons:** Primary buttons use the Deep Teal (#006D77) background with white text. Secondary buttons use a thick 2px Neutral border with no fill. All buttons use 12px vertical and 24px horizontal padding.
*   **Input Fields:** Clean white backgrounds with 1px #D1D5DB borders. Use icons (e.g., search, weight scale, clock) in a muted #6B7280 color positioned on the left of the text.
*   **Cards:** The fundamental unit for exercises. Features a white background, 8px radius, and a 1px border. Headlines inside cards should be Semi-bold 18px.
*   **Navigation Bar:** A fixed-top white bar with a high-contrast bottom border (1px #E5E7EB). The 'Gym Buddy' wordmark is placed on the left in Inter Bold, Neutral color.
*   **Chips:** Used for muscle groups (e.g., "Chest", "Triceps"). Small, 4px rounded shapes with #F3F4F6 backgrounds and #4B5563 text.
*   **Progress Bars:** Thin 8px height tracks in #E5E7EB with a Primary Teal fill to show set completion or goal progress.