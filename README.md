# GéraldMag

A tool for creating complex and large documents (like magazines) using WeasyPrint under the hood. GéraldMag is inspired by static site generators but focuses on producing a single PDF output instead of multiple HTML pages.

## Features

- Simple command-line interface built with Click
- SCSS transformation to CSS2
- Markdown content support (with more engines planned for future releases)
- Jinja2 templating for flexible document composition
- Configuration using TOML

## Installation

```bash
pip install geraldmag
```

## Quick Start

1. Create a project with the recommended structure
2. Configure your publication in `mag.toml`
3. Build your publication: `geraldmag build <publication-name>`

## Project Structure

```plaintext
my-magazine/
├── mag.toml                  # Main configuration file
├── content/                  # Content directory
│   ├── _default/             # Default templates and styles (optional)
│   │   └── styles/           # Default stylesheets
│   └── mag202504/            # A publication directory
│       ├── index.html        # Entry point for the publication
│       ├── articles/         # Content organized by sections
│       │   └── myarticle/
│       │       ├── index.md  # Markdown content
│       │       └── image.jpg # Images used in the article
│       └── styles/           # Publication-specific styles
```

## Content Organization

- `mag.toml`: Configuration file at the root of your project
- `content/`: Main directory that holds all your content
- `content/_default/`: Optional directory with default templates and styles
- `content/<publication>/`: Directory for each publication (e.g., magazine issue)
  - `index.html`: The main template for the publication
  - Additional directories for articles, images, and other resources

## How It Works

1. The CLI is called with the name of a publication: `geraldmag build mag202504`
2. The program reads the `mag.toml` configuration file
3. The program processes the `index.html` file, which may contain Jinja2 template directives
4. Using Jinja2, a single consolidated HTML file is created in `_resources/<publication>/` along with all necessary assets
5. The HTML file is passed to WeasyPrint for conversion to a PDF output in `out/<publication>.pdf`

## Configuration (mag.toml)

```toml
# Basic configuration
title = "My Magazine"
content_dir = "content"
default_dir = "_default"
resources_dir = "_resources"
output_dir = "out"

# Publication-specific settings can be defined
[publications.issue2025]
title = "Spring Issue 2025"
output = "magazine-spring-2025.pdf"
```

## Command Line Usage

```bash
# Setup your project
geraldmag init

# Scaffold a new publication
geraldmag new mag202504

# Build a specific publication
geraldmag build mag202504

# Show version information
geraldmag --version
```

## Templating

GéraldMag uses Jinja2 for templating. You can include content from Markdown files:

```html
<article>
  {% include 'articles/myarticle/index.md' %}
</article>
```

## Styling

Use SCSS for your styles, which will be automatically compiled to CSS2:

```scss
// styles/main.scss
$primary-color: #336699;

.article {
  color: $primary-color;
  h1 {
    font-size: 24pt;
  }
}
```

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
