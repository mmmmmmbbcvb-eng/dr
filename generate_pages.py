import os
import json

# Load CSS
with open('styles_template.css', 'r') as f:
    css_content = f.read()

# Shared JS for search, filtering, etc.
shared_js = """
const toolsData = %s;

document.addEventListener('DOMContentLoaded', () => {
    const grid = document.getElementById('tools-grid');
    const searchInput = document.getElementById('search-input');
    const filterButtons = document.querySelectorAll('.filter-btn');
    const backToTop = document.getElementById('back-to-top');
    const loadingOverlay = document.getElementById('loading-overlay');

    // Smooth Scroll
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Back to Top
    window.onscroll = () => {
        if (document.body.scrollTop > 500 || document.documentElement.scrollTop > 500) {
            backToTop.style.display = "flex";
        } else {
            backToTop.style.display = "none";
        }
    };

    backToTop.onclick = () => {
        window.scrollTo({top: 0, behavior: 'smooth'});
    };

    // Rendering Function
    function renderTools(tools) {
        if (!grid) return;
        grid.innerHTML = '';
        
        if (tools.length === 0) {
            grid.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 3rem; color: var(--secondary-text);">No tools found matching your criteria.</div>';
            return;
        }

        tools.forEach(tool => {
            const card = document.createElement('div');
            card.className = 'card';
            card.innerHTML = `
                <div class="card-header" style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                    <img src="${tool.logo}" alt="${tool.name}" style="width: 48px; height: 48px; border-radius: 10px; object-fit: cover; background: #222;" loading="lazy">
                    <div>
                        <h3 style="font-size: 1.1rem;">${tool.name}</h3>
                        <span style="color: var(--accent-color); font-size: 0.8rem; font-weight: 600;">${tool.category}</span>
                    </div>
                </div>
                <p style="color: var(--secondary-text); font-size: 0.9rem; margin-bottom: 1rem; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; height: 2.8rem;">${tool.description}</p>
                <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
                    <span style="color: #FFD700;">★</span>
                    <span style="font-weight: 600;">${tool.rating}</span>
                    <div style="display: flex; gap: 0.3rem; margin-left: auto;">
                        ${tool.tags.slice(0, 2).map(tag => `<span style="background: #222; padding: 2px 8px; border-radius: 4px; font-size: 0.7rem;">${tag}</span>`).join('')}
                    </div>
                </div>
                <div style="display: flex; gap: 0.5rem;">
                    <a href="${tool.url}" class="btn btn-primary" style="flex: 1; font-size: 0.8rem; padding: 0.6rem;" target="_blank">Visit</a>
                    <button class="btn btn-secondary save-btn" style="padding: 0.6rem;" onclick="toggleSave(${tool.id})">
                        <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M2 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v13.5a.5.5 0 0 1-.777.416L8 13.101l-5.223 2.815A.5.5 0 0 1 2 15.5V2z"/></svg>
                    </button>
                    <button class="btn btn-secondary share-btn" style="padding: 0.6rem;" onclick="shareTool('${tool.name}')">
                        <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M13.5 1a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3zM11 2.5a2.5 2.5 0 1 1 .603 1.628l-6.718 3.12a2.499 2.499 0 0 1 0 1.504l6.718 3.12a2.5 2.5 0 1 1-.488.876l-6.718-3.12a2.5 2.5 0 1 1 0-3.256l6.718-3.12A2.5 2.5 0 0 1 11 2.5zm-8.5 4a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3zm11 5.5a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3z"/></svg>
                    </button>
                </div>
            `;
            grid.appendChild(card);
        });
    }

    // Search Functionality
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const term = e.target.value.toLowerCase();
            const filtered = toolsData.filter(t => 
                t.name.toLowerCase().includes(term) || 
                t.description.toLowerCase().includes(term) ||
                t.tags.some(tag => tag.toLowerCase().includes(term))
            );
            renderTools(filtered);
        });
    }

    // Filter Functionality
    filterButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            filterButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const category = btn.dataset.category;
            const filtered = category === 'all' ? toolsData : toolsData.filter(t => t.category === category);
            renderTools(filtered);
        });
    });

    // Initial Render
    setTimeout(() => {
        if (loadingOverlay) loadingOverlay.style.opacity = '0';
        setTimeout(() => { if (loadingOverlay) loadingOverlay.style.display = 'none'; }, 500);
        
        // Page specific logic
        const path = window.location.pathname;
        let initialData = toolsData;
        
        if (path.includes('ai-tools')) initialData = toolsData.filter(t => t.category === 'AI');
        else if (path.includes('mobile-apps')) initialData = toolsData.filter(t => t.category === 'Android' || t.category === 'iOS');
        else if (path.includes('apis')) initialData = toolsData.filter(t => t.category === 'APIs');
        else if (path.includes('learning')) initialData = toolsData.filter(t => t.category === 'Learning');
        
        renderTools(initialData);
    }, 1000);
});

function toggleSave(id) {
    alert('Tool saved to favorites!');
}

function shareTool(name) {
    alert('Sharing ' + name);
}
"""

# HTML Template Parts
def get_header(title, active_page):
    return f'''
    <header class="header glass">
        <div class="logo" style="font-family: var(--font-display); font-weight: 800; font-size: 1.5rem; color: var(--accent-color);">
            DevHub
        </div>
        <div class="search-container" style="flex: 0.6; position: relative;">
            <input type="text" id="search-input" placeholder="Search for tools, APIs, resources..." style="width: 100%; padding: 0.8rem 1rem 0.8rem 2.5rem; background: #111; border: 1px solid var(--border-color); border-radius: 10px; color: white; outline: none;">
            <svg style="position: absolute; left: 0.8rem; top: 50%; transform: translateY(-50%); color: var(--secondary-text);" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z"/></svg>
        </div>
        <div class="user-actions" style="display: flex; gap: 1rem;">
            <a href="favorites.html" class="btn btn-secondary" style="padding: 0.5rem 1rem;">Favorites</a>
            <a href="contact.html" class="btn btn-primary" style="padding: 0.5rem 1rem;">Submit Tool</a>
        </div>
    </header>
    '''

def get_sidebar(active_page):
    links = [
        ("Home", "index.html"),
        ("Explore", "explore.html"),
        ("Categories", "categories.html"),
        ("AI Tools", "ai-tools.html"),
        ("Websites", "websites.html"),
        ("Mobile Apps", "mobile-apps.html"),
        ("APIs", "apis.html"),
        ("Open Source", "open-source.html"),
        ("GitHub Projects", "github-projects.html"),
        ("Learning", "learning.html"),
        ("Blog", "blog.html"),
        ("About", "about.html"),
        ("Contact", "contact.html")
    ]
    
    sidebar_html = '<div class="sidebar glass">'
    sidebar_html += '<div style="margin-bottom: 2rem; font-family: var(--font-display); font-weight: 800; font-size: 1.8rem;">DevHub</div>'
    sidebar_html += '<nav style="display: flex; flex-direction: column; gap: 0.5rem;">'
    
    for name, url in links:
        is_active = "background: var(--accent-color); color: white;" if name == active_page else "color: var(--secondary-text);"
        sidebar_html += f'<a href="{url}" style="text-decoration: none; padding: 0.8rem 1rem; border-radius: 8px; font-weight: 500; transition: var(--transition); {is_active}">{name}</a>'
    
    sidebar_html += '</nav></div>'
    return sidebar_html

def get_bottom_nav():
    return '''
    <nav class="bottom-nav glass">
        <a href="index.html" style="color: var(--accent-color); display: flex; flex-direction: column; align-items: center; font-size: 0.7rem; text-decoration: none;">
            <svg width="24" height="24" fill="currentColor" viewBox="0 0 16 16"><path d="M8.707 1.5a1 1 0 0 0-1.414 0L.646 8.146a.5.5 0 0 0 .708.708L2 8.207V13.5A1.5 1.5 0 0 0 3.5 15h9a1.5 1.5 0 0 0 1.5-1.5V8.207l.646.647a.5.5 0 0 0 .708-.708L13 5.793V2.5a.5.5 0 0 0-.5-.5h-1a.5.5 0 0 0-.5.5v1.293L8.707 1.5Z"/></svg>
            Home
        </a>
        <a href="explore.html" style="color: var(--secondary-text); display: flex; flex-direction: column; align-items: center; font-size: 0.7rem; text-decoration: none;">
            <svg width="24" height="24" fill="currentColor" viewBox="0 0 16 16"><path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/><path d="M4.285 9.567a.5.5 0 0 1 .683.183A3.498 3.498 0 0 0 8 11.5a3.498 3.498 0 0 0 3.032-1.75.5.5 0 1 1 .866.5A4.498 4.498 0 0 1 8 12.5a4.498 4.498 0 0 1-3.898-2.25.5.5 0 0 1 .183-.683z"/></svg>
            Explore
        </a>
        <a href="categories.html" style="color: var(--secondary-text); display: flex; flex-direction: column; align-items: center; font-size: 0.7rem; text-decoration: none;">
            <svg width="24" height="24" fill="currentColor" viewBox="0 0 16 16"><path d="M1 2.5A1.5 1.5 0 0 1 2.5 1h3A1.5 1.5 0 0 1 7 2.5v3A1.5 1.5 0 0 1 5.5 7h-3A1.5 1.5 0 0 1 1 5.5v-3zM2.5 2a.5.5 0 0 0-.5.5v3a.5.5 0 0 0 .5.5h3a.5.5 0 0 0 .5-.5v-3a.5.5 0 0 0-.5-.5h-3zm6.5.5A1.5 1.5 0 0 1 10.5 1h3A1.5 1.5 0 0 1 15 2.5v3A1.5 1.5 0 0 1 13.5 7h-3A1.5 1.5 0 0 1 9 5.5v-3zm1.5-.5a.5.5 0 0 0-.5.5v3a.5.5 0 0 0 .5.5h3a.5.5 0 0 0 .5-.5v-3a.5.5 0 0 0-.5-.5h-3zM1 10.5A1.5 1.5 0 0 1 2.5 9h3A1.5 1.5 0 0 1 7 10.5v3A1.5 1.5 0 0 1 5.5 15h-3A1.5 1.5 0 0 1 1 13.5v-3zm1.5-.5a.5.5 0 0 0-.5.5v3a.5.5 0 0 0 .5.5h3a.5.5 0 0 0 .5-.5v-3a.5.5 0 0 0-.5-.5h-3zm6.5.5A1.5 1.5 0 0 1 10.5 9h3a1.5 1.5 0 0 1 1.5 1.5v3a1.5 1.5 0 0 1-1.5 1.5h-3A1.5 1.5 0 0 1 9 13.5v-3zm1.5-.5a.5.5 0 0 0-.5.5v3a.5.5 0 0 0 .5.5h3a.5.5 0 0 0 .5-.5v-3a.5.5 0 0 0-.5-.5h-3z"/></svg>
            Apps
        </a>
        <a href="favorites.html" style="color: var(--secondary-text); display: flex; flex-direction: column; align-items: center; font-size: 0.7rem; text-decoration: none;">
            <svg width="24" height="24" fill="currentColor" viewBox="0 0 16 16"><path d="M2 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v13.5a.5.5 0 0 1-.777.416L8 13.101l-5.223 2.815A.5.5 0 0 1 2 15.5V2z"/></svg>
            Saved
        </a>
    </nav>
    '''

def get_footer():
    return '''
    <footer style="margin-top: 5rem; padding: 4rem 2rem; border-top: 1px solid var(--border-color); background: #080808;">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 3rem; max-width: 1200px; margin: 0 auto;">
            <div>
                <h3 style="margin-bottom: 1.5rem; color: var(--accent-color);">DevHub</h3>
                <p style="color: var(--secondary-text); font-size: 0.9rem;">The ultimate collection of tools and resources for developers and designers. Built for the community.</p>
            </div>
            <div>
                <h4 style="margin-bottom: 1.2rem;">Resources</h4>
                <ul style="list-style: none; display: flex; flex-direction: column; gap: 0.8rem; font-size: 0.9rem;">
                    <li><a href="explore.html" style="color: var(--secondary-text); text-decoration: none;">Explore Tools</a></li>
                    <li><a href="apis.html" style="color: var(--secondary-text); text-decoration: none;">APIs Directory</a></li>
                    <li><a href="learning.html" style="color: var(--secondary-text); text-decoration: none;">Learning Paths</a></li>
                    <li><a href="blog.html" style="color: var(--secondary-text); text-decoration: none;">Dev Blog</a></li>
                </ul>
            </div>
            <div>
                <h4 style="margin-bottom: 1.2rem;">Community</h4>
                <ul style="list-style: none; display: flex; flex-direction: column; gap: 0.8rem; font-size: 0.9rem;">
                    <li><a href="open-source.html" style="color: var(--secondary-text); text-decoration: none;">Open Source</a></li>
                    <li><a href="github-projects.html" style="color: var(--secondary-text); text-decoration: none;">GitHub Showcase</a></li>
                    <li><a href="contact.html" style="color: var(--secondary-text); text-decoration: none;">Submit Tool</a></li>
                </ul>
            </div>
            <div>
                <h4 style="margin-bottom: 1.2rem;">Legal</h4>
                <ul style="list-style: none; display: flex; flex-direction: column; gap: 0.8rem; font-size: 0.9rem;">
                    <li><a href="#" style="color: var(--secondary-text); text-decoration: none;">Privacy Policy</a></li>
                    <li><a href="#" style="color: var(--secondary-text); text-decoration: none;">Terms of Service</a></li>
                </ul>
            </div>
        </div>
        <div style="text-align: center; margin-top: 4rem; padding-top: 2rem; border-top: 1px solid #111; color: var(--secondary-text); font-size: 0.8rem;">
            &copy; 2026 DevHub. All rights reserved. Designed with ❤️ for Developers.
        </div>
    </footer>
    '''

def generate_page(name, title, content_html, active_page, tools_data_json):
    html = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | DevHub - Best Programming Tools</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        {css_content}
        
        /* Skeleton Loading Animation */
        @keyframes shimmer {{
            0% {{ background-position: -468px 0; }}
            100% {{ background-position: 468px 0; }}
        }}
        .skeleton {{
            background: #1a1a1a;
            background-image: linear-gradient(to right, #1a1a1a 0%, #222 20%, #1a1a1a 40%, #1a1a1a 100%);
            background-repeat: no-repeat;
            background-size: 800px 104px;
            display: inline-block;
            position: relative;
            animation: shimmer 1s linear infinite forwards;
        }}
        
        #loading-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: #000;
            z-index: 9999;
            display: flex;
            justify-content: center;
            align-items: center;
            transition: opacity 0.5s ease;
        }}
        
        .loader {{
            width: 48px;
            height: 48px;
            border: 3px solid var(--accent-color);
            border-bottom-color: transparent;
            border-radius: 50%;
            display: inline-block;
            box-sizing: border-box;
            animation: rotation 1s linear infinite;
        }}
        
        @keyframes rotation {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        
        #back-to-top {{
            position: fixed;
            bottom: 90px;
            right: 20px;
            width: 45px;
            height: 45px;
            background: var(--accent-color);
            color: white;
            border-radius: 50%;
            display: none;
            justify-content: center;
            align-items: center;
            cursor: pointer;
            z-index: 99;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }}
    </style>
</head>
<body>
    <div id="loading-overlay">
        <span class="loader"></span>
    </div>

    <div class="app-container">
        {get_sidebar(active_page)}
        
        <main class="main-content">
            {get_header(title, active_page)}
            
            {content_html}
            
            {get_footer()}
        </main>
    </div>

    {get_bottom_nav()}
    
    <div id="back-to-top">
        <svg width="24" height="24" fill="currentColor" viewBox="0 0 16 16"><path d="M8 15a.5.5 0 0 0 .5-.5V2.707l3.146 3.147a.5.5 0 0 0 .708-.708l-4-4a.5.5 0 0 0-.708 0l-4 4a.5.5 0 1 0 .708.708L7.5 2.707V14.5a.5.5 0 0 0 .5.5z"/></svg>
    </div>

    <script>
        {shared_js % tools_data_json}
    </script>
</body>
</html>
    '''
    with open(name, 'w') as f:
        f.write(html)

# Tools Data
import json

tools_data = [
    {"id": 1, "name": "ChatGPT", "logo": "https://upload.wikimedia.org/wikipedia/commons/0/04/ChatGPT_logo.svg", "description": "Advanced AI language model by OpenAI for conversation and task automation.", "category": "AI", "rating": 4.9, "tags": ["LLM", "OpenAI", "Chat"], "url": "https://chat.openai.com"},
    {"id": 2, "name": "Midjourney", "logo": "https://upload.wikimedia.org/wikipedia/commons/e/e6/Midjourney_Emblem.svg", "description": "Generative AI for creating high-quality artistic images from text prompts.", "category": "AI", "rating": 4.8, "tags": ["Images", "Art", "Design"], "url": "https://midjourney.com"},
    {"id": 3, "name": "Claude AI", "logo": "https://upload.wikimedia.org/wikipedia/commons/d/d4/Anthropic_logo.svg", "description": "Constitutional AI by Anthropic focusing on safety and long-context understanding.", "category": "AI", "rating": 4.7, "tags": ["LLM", "Safety", "Research"], "url": "https://claude.ai"},
    {"id": 4, "name": "GitHub Copilot", "logo": "https://github.githubassets.com/images/modules/site/features/copilot/copilot-logo.png", "description": "AI pair programmer that helps you write code faster with less work.", "category": "AI", "rating": 4.9, "tags": ["Coding", "GitHub", "Autocompletion"], "url": "https://github.com/features/copilot"},
    {"id": 5, "name": "Jasper", "logo": "https://www.jasper.ai/favicon.ico", "description": "AI content platform that helps teams create high-quality content faster.", "category": "AI", "rating": 4.5, "tags": ["Marketing", "Writing", "Business"], "url": "https://jasper.ai"},
    {"id": 6, "name": "VS Code", "logo": "https://upload.wikimedia.org/wikipedia/commons/9/9a/Visual_Studio_Code_1.35_icon.svg", "description": "The most popular code editor with extensive plugin ecosystem.", "category": "Web Development", "rating": 5.0, "tags": ["Editor", "Microsoft", "Free"], "url": "https://code.visualstudio.com"},
    {"id": 7, "name": "Next.js", "logo": "https://assets.vercel.com/image/upload/v1662130559/nextjs/Icon_light_background.png", "description": "The React Framework for the Web, optimized for performance and SEO.", "category": "Web Development", "rating": 4.8, "tags": ["React", "Framework", "Vercel"], "url": "https://nextjs.org"},
    {"id": 8, "name": "Tailwind CSS", "logo": "https://upload.wikimedia.org/wikipedia/commons/d/d5/Tailwind_CSS_Logo.svg", "description": "A utility-first CSS framework for rapid UI development.", "category": "Web Development", "rating": 4.9, "tags": ["CSS", "Design", "Frontend"], "url": "https://tailwindcss.com"},
    {"id": 9, "name": "Vercel", "logo": "https://assets.vercel.com/image/upload/v1588805177/repositories/vercel/logo.png", "description": "Platform for frontend developers to deploy and scale instantly.", "category": "Web Development", "rating": 4.7, "tags": ["Hosting", "Deployment", "CI/CD"], "url": "https://vercel.com"},
    {"id": 10, "name": "Figma", "logo": "https://upload.wikimedia.org/wikipedia/commons/3/33/Figma-logo.svg", "description": "Collaborative interface design tool for teams.", "category": "Design", "rating": 4.9, "tags": ["UI", "UX", "Prototyping"], "url": "https://figma.com"},
    {"id": 11, "name": "Stripe API", "logo": "https://upload.wikimedia.org/wikipedia/commons/b/ba/Stripe_Logo%2C_revised_2016.svg", "description": "Financial infrastructure for the internet to accept payments.", "category": "APIs", "rating": 4.9, "tags": ["Payments", "Finance", "SDK"], "url": "https://stripe.com"},
    {"id": 12, "name": "Twilio", "logo": "https://upload.wikimedia.org/wikipedia/commons/7/7e/Twilio-logo.svg", "description": "Communication APIs for SMS, Voice, Video, and Authentication.", "category": "APIs", "rating": 4.6, "tags": ["SMS", "Communication", "Auth"], "url": "https://twilio.com"},
    {"id": 13, "name": "Google Maps API", "logo": "https://upload.wikimedia.org/wikipedia/commons/a/aa/Google_Maps_icon_%282020%29.svg", "description": "Build real-world map experiences with location data.", "category": "APIs", "rating": 4.7, "tags": ["Maps", "Location", "Google"], "url": "https://developers.google.com/maps"},
    {"id": 14, "name": "Spotify API", "logo": "https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg", "description": "Access data from the Spotify music catalog and manage user playlists.", "category": "APIs", "rating": 4.5, "tags": ["Music", "Data", "Entertainment"], "url": "https://developer.spotify.com"},
    {"id": 15, "name": "freeCodeCamp", "logo": "https://upload.wikimedia.org/wikipedia/commons/3/39/FreeCodeCamp_logo.png", "description": "Learn to code for free with thousands of tutorials and certifications.", "category": "Learning", "rating": 5.0, "tags": ["Education", "Free", "Certificates"], "url": "https://freecodecamp.org"},
    {"id": 16, "name": "Udemy", "logo": "https://upload.wikimedia.org/wikipedia/commons/e/e3/Udemy_logo.svg", "description": "Online learning and teaching marketplace with 213,000+ courses.", "category": "Learning", "rating": 4.4, "tags": ["Courses", "Paid", "Skills"], "url": "https://udemy.com"},
    {"id": 17, "name": "Coursera", "logo": "https://upload.wikimedia.org/wikipedia/commons/9/97/Coursera-Logo_600x600.svg", "description": "Learn without limits with online degrees and certificates.", "category": "Learning", "rating": 4.6, "tags": ["University", "Degrees", "Academic"], "url": "https://coursera.org"},
    {"id": 18, "name": "Flutter", "logo": "https://upload.wikimedia.org/wikipedia/commons/1/17/Google-flutter-logo.svg", "description": "Google's UI toolkit for building natively compiled applications.", "category": "iOS", "rating": 4.8, "tags": ["Mobile", "Cross-platform", "Google"], "url": "https://flutter.dev"},
    {"id": 19, "name": "React Native", "logo": "https://upload.wikimedia.org/wikipedia/commons/a/a7/React-icon.svg", "description": "Create native apps for Android and iOS using React.", "category": "Android", "rating": 4.7, "tags": ["Mobile", "React", "Meta"], "url": "https://reactnative.dev"},
    {"id": 20, "name": "Docker", "logo": "https://upload.wikimedia.org/wikipedia/commons/4/4e/Docker_%28container_engine%29_logo.svg", "description": "OS-level virtualization to deliver software in packages called containers.", "category": "DevOps", "rating": 4.9, "tags": ["Containers", "Infrastructure", "Scaling"], "url": "https://docker.com"},
    {"id": 21, "name": "AWS", "logo": "https://upload.wikimedia.org/wikipedia/commons/9/93/Amazon_Web_Services_Logo.svg", "description": "Comprehensive and broadly adopted cloud platform.", "category": "Cloud", "rating": 4.8, "tags": ["Infrastructure", "Serverless", "Amazon"], "url": "https://aws.amazon.com"},
    {"id": 22, "name": "Terraform", "logo": "https://upload.wikimedia.org/wikipedia/commons/0/04/Terraform_Logo.svg", "description": "Infrastructure as Code tool for building and changing infrastructure safely.", "category": "DevOps", "rating": 4.7, "tags": ["IaC", "HashiCorp", "Automation"], "url": "https://terraform.io"},
    {"id": 23, "name": "Supabase", "logo": "https://seeklogo.com/images/S/supabase-logo-DCC416CAB2-seeklogo.com.png", "description": "The open source Firebase alternative with Postgres.", "category": "Database", "rating": 4.9, "tags": ["Postgres", "Auth", "Realtime"], "url": "https://supabase.com"},
    {"id": 24, "name": "MongoDB", "logo": "https://upload.wikimedia.org/wikipedia/commons/9/93/MongoDB_Logo.svg", "description": "The most popular NoSQL database for modern applications.", "category": "Database", "rating": 4.6, "tags": ["NoSQL", "JSON", "Cloud"], "url": "https://mongodb.com"},
    {"id": 25, "name": "PlanetScale", "logo": "https://planetscale.com/favicon.ico", "description": "The world's most advanced serverless MySQL platform.", "category": "Database", "rating": 4.7, "tags": ["MySQL", "Serverless", "Scaling"], "url": "https://planetscale.com"},
    {"id": 26, "name": "Auth0", "logo": "https://upload.wikimedia.org/wikipedia/commons/a/a2/Auth0_logo.svg", "description": "Identity platform for application builders.", "category": "Security", "rating": 4.5, "tags": ["Auth", "Identity", "Okta"], "url": "https://auth0.com"},
    {"id": 27, "name": "Snyk", "logo": "https://snyk.io/styleguide/assets/logos/snyk-logo-black.svg", "description": "Developer-first security platform for scanning code and dependencies.", "category": "Security", "rating": 4.6, "tags": ["Scanning", "DevSecOps", "Vulnerabilities"], "url": "https://snyk.io"},
    {"id": 28, "name": "Notion", "logo": "https://upload.wikimedia.org/wikipedia/commons/4/45/Notion_app_logo.png", "description": "The all-in-one workspace for notes, tasks, and wikis.", "category": "Productivity", "rating": 4.9, "tags": ["Workspace", "Notes", "Collaboration"], "url": "https://notion.so"},
    {"id": 29, "name": "Slack", "logo": "https://upload.wikimedia.org/wikipedia/commons/d/d5/Slack_icon_2019.svg", "description": "Where work happens - team communication and collaboration.", "category": "Productivity", "rating": 4.7, "tags": ["Chat", "Team", "Business"], "url": "https://slack.com"},
    {"id": 30, "name": "Trello", "logo": "https://upload.wikimedia.org/wikipedia/commons/7/7a/Trello-logo-blue.svg", "description": "Visual tool for managing projects and organizing anything.", "category": "Productivity", "rating": 4.5, "tags": ["Kanban", "Tasks", "Project"], "url": "https://trello.com"}
]

for i in range(31, 111):
    cats = ["AI", "Web Development", "Android", "iOS", "Backend", "Frontend", "Design", "UI/UX", "APIs", "Database", "Cloud", "DevOps", "Productivity", "Security", "Learning"]
    cat = cats[i % len(cats)]
    tools_data.append({
        "id": i,
        "name": f"{cat} Tool {i}",
        "logo": f"https://picsum.photos/seed/{i}/100/100",
        "description": f"This is a high-performance tool for {cat}. It helps developers streamline their workflow and achieve better results in less time.",
        "category": cat,
        "rating": 4.5,
        "tags": [cat, "DevTool", "Modern"],
        "url": "#"
    })

final_json = json.dumps(tools_data)

# Home Page Content
home_content = '''
<section class="hero" style="padding: 4rem 2rem; text-align: center; background: radial-gradient(circle at center, #111 0%, #000 70%); border-bottom: 1px solid var(--border-color);">
    <h1 style="font-size: 4rem; margin-bottom: 1rem; background: linear-gradient(to right, #fff, #888); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Build Better. Faster.</h1>
    <p style="color: var(--secondary-text); font-size: 1.2rem; max-width: 700px; margin: 0 auto 2.5rem;">The curated collection of premium tools, APIs, and resources for the modern developer ecosystem.</p>
    <div style="display: flex; gap: 1rem; justify-content: center;">
        <a href="explore.html" class="btn btn-primary" style="padding: 1rem 2rem; font-size: 1.1rem;">Explore All Tools</a>
        <a href="categories.html" class="btn btn-secondary" style="padding: 1rem 2rem; font-size: 1.1rem;">Browse Categories</a>
    </div>
</section>

<section style="padding: 4rem 0;">
    <div style="padding: 0 2rem; display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;">
        <h2 class="section-title">Featured Tools</h2>
        <a href="explore.html" style="color: var(--accent-color); text-decoration: none; font-weight: 600;">View All →</a>
    </div>
    <div id="tools-grid" class="grid">
        <!-- Skeleton cards -->
        <div class="card"><div class="skeleton" style="width: 100%; height: 200px; border-radius: 8px;"></div></div>
        <div class="card"><div class="skeleton" style="width: 100%; height: 200px; border-radius: 8px;"></div></div>
        <div class="card"><div class="skeleton" style="width: 100%; height: 200px; border-radius: 8px;"></div></div>
    </div>
</section>

<section style="padding: 4rem 2rem; background: #080808; border-top: 1px solid var(--border-color); border-bottom: 1px solid var(--border-color);">
    <h2 class="section-title" style="text-align: center;">Popular Categories</h2>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin-top: 2rem;">
        <a href="ai-tools.html" style="background: #161616; padding: 2rem; border-radius: 12px; text-align: center; text-decoration: none; border: 1px solid var(--border-color); transition: var(--transition);" onmouseover="this.style.borderColor='var(--accent-color)'" onmouseout="this.style.borderColor='var(--border-color)'">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🤖</div>
            <div style="color: white; font-weight: 600;">AI Tools</div>
        </a>
        <a href="websites.html" style="background: #161616; padding: 2rem; border-radius: 12px; text-align: center; text-decoration: none; border: 1px solid var(--border-color); transition: var(--transition);" onmouseover="this.style.borderColor='var(--accent-color)'" onmouseout="this.style.borderColor='var(--border-color)'">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🌐</div>
            <div style="color: white; font-weight: 600;">Websites</div>
        </a>
        <a href="mobile-apps.html" style="background: #161616; padding: 2rem; border-radius: 12px; text-align: center; text-decoration: none; border: 1px solid var(--border-color); transition: var(--transition);" onmouseover="this.style.borderColor='var(--accent-color)'" onmouseout="this.style.borderColor='var(--border-color)'">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">📱</div>
            <div style="color: white; font-weight: 600;">Mobile Apps</div>
        </a>
        <a href="apis.html" style="background: #161616; padding: 2rem; border-radius: 12px; text-align: center; text-decoration: none; border: 1px solid var(--border-color); transition: var(--transition);" onmouseover="this.style.borderColor='var(--accent-color)'" onmouseout="this.style.borderColor='var(--border-color)'">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔌</div>
            <div style="color: white; font-weight: 600;">APIs</div>
        </a>
        <a href="learning.html" style="background: #161616; padding: 2rem; border-radius: 12px; text-align: center; text-decoration: none; border: 1px solid var(--border-color); transition: var(--transition);" onmouseover="this.style.borderColor='var(--accent-color)'" onmouseout="this.style.borderColor='var(--border-color)'">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">📚</div>
            <div style="color: white; font-weight: 600;">Learning</div>
        </a>
    </div>
</section>

<section style="padding: 6rem 2rem; text-align: center;">
    <div class="glass" style="max-width: 800px; margin: 0 auto; padding: 4rem 2rem; border-radius: 24px;">
        <h2 style="font-size: 2.5rem; margin-bottom: 1rem;">Stay ahead of the curve</h2>
        <p style="color: var(--secondary-text); margin-bottom: 2rem;">Get weekly updates on the latest developer tools and resources.</p>
        <form style="display: flex; gap: 0.5rem; max-width: 500px; margin: 0 auto;">
            <input type="email" placeholder="Enter your email" style="flex: 1; padding: 1rem; border-radius: 8px; border: 1px solid var(--border-color); background: #000; color: white; outline: none;">
            <button type="submit" class="btn btn-primary">Subscribe</button>
        </form>
    </div>
</section>
'''

# Generic Content for other pages
def get_generic_content(title, show_filters=True):
    filters = ''
    if show_filters:
        cats = ["all", "AI", "Web Development", "Android", "iOS", "Backend", "Frontend", "Design", "UI/UX", "APIs", "Database", "Cloud", "DevOps", "Productivity", "Security", "Learning"]
        filters = '<div style="display: flex; gap: 0.8rem; overflow-x: auto; padding: 0 2rem 2rem; scrollbar-width: none;">'
        for cat in cats:
            active = 'active' if cat == 'all' else ''
            filters += f'<button class="filter-btn {active}" data-category="{cat}" style="white-space: nowrap; padding: 0.6rem 1.2rem; border-radius: 20px; border: 1px solid var(--border-color); background: transparent; color: var(--secondary-text); cursor: pointer; transition: var(--transition);">{cat}</button>'
        filters += '</div>'
        
        # Style for active filter
        filters += '<style>.filter-btn.active { background: var(--accent-color) !important; color: white !important; border-color: var(--accent-color) !important; }</style>'

    return f'''
    <section style="padding: 3rem 0;">
        <div style="padding: 0 2rem; margin-bottom: 2rem;">
            <h1 class="section-title">{title}</h1>
            <p style="color: var(--secondary-text);">Discover the best resources in this category.</p>
        </div>
        {filters}
        <div id="tools-grid" class="grid">
            <!-- Content loaded via JS -->
        </div>
    </section>
    '''

# Generate all pages
pages = [
    ("index.html", "Home", home_content, "Home"),
    ("explore.html", "Explore Tools", get_generic_content("Explore All Tools"), "Explore"),
    ("categories.html", "Categories", get_generic_content("Browse by Category"), "Categories"),
    ("ai-tools.html", "AI Tools", get_generic_content("AI & Machine Learning", False), "AI Tools"),
    ("websites.html", "Websites", get_generic_content("Useful Developer Websites", False), "Websites"),
    ("mobile-apps.html", "Mobile Apps", get_generic_content("Mobile Development Apps", False), "Mobile Apps"),
    ("apis.html", "APIs", get_generic_content("Public & Developer APIs", False), "APIs"),
    ("open-source.html", "Open Source", get_generic_content("Open Source Projects"), "Open Source"),
    ("github-projects.html", "GitHub Projects", get_generic_content("Trending GitHub Repos"), "GitHub Projects"),
    ("learning.html", "Learning Resources", get_generic_content("Learn Programming", False), "Learning"),
    ("blog.html", "Developer Blog", get_generic_content("Latest Dev News"), "Blog"),
    ("favorites.html", "My Favorites", get_generic_content("Your Saved Tools"), "Favorites"),
    ("about.html", "About Us", '<section style="padding: 4rem 2rem; max-width: 800px; margin: 0 auto;"><h1>About DevHub</h1><p style="margin-top: 2rem; color: var(--secondary-text);">DevHub is a curated directory of tools for developers. Our mission is to help developers find the best resources to build their next big thing.</p></section>', "About"),
    ("contact.html", "Contact Us", '<section style="padding: 4rem 2rem; max-width: 600px; margin: 0 auto;"><h1>Get in Touch</h1><form style="margin-top: 2rem; display: flex; flex-direction: column; gap: 1.5rem;"><input type="text" placeholder="Name" style="padding: 1rem; border-radius: 8px; border: 1px solid var(--border-color); background: #111; color: white;"><input type="email" placeholder="Email" style="padding: 1rem; border-radius: 8px; border: 1px solid var(--border-color); background: #111; color: white;"><textarea placeholder="Message" rows="5" style="padding: 1rem; border-radius: 8px; border: 1px solid var(--border-color); background: #111; color: white;"></textarea><button type="submit" class="btn btn-primary">Send Message</button></form></section>', "Contact")
]

for filename, title, content, active in pages:
    generate_page(filename, title, content, active, final_json)

print("All 14 pages generated successfully.")
