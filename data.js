const toolsData = [
    // AI Tools
    { id: 1, name: "ChatGPT", logo: "https://upload.wikimedia.org/wikipedia/commons/0/04/ChatGPT_logo.svg", description: "Advanced AI language model by OpenAI for conversation and task automation.", category: "AI", rating: 4.9, tags: ["LLM", "OpenAI", "Chat"], url: "https://chat.openai.com" },
    { id: 2, name: "Midjourney", logo: "https://upload.wikimedia.org/wikipedia/commons/e/e6/Midjourney_Emblem.svg", description: "Generative AI for creating high-quality artistic images from text prompts.", category: "AI", rating: 4.8, tags: ["Images", "Art", "Design"], url: "https://midjourney.com" },
    { id: 3, name: "Claude AI", logo: "https://upload.wikimedia.org/wikipedia/commons/d/d4/Anthropic_logo.svg", description: "Constitutional AI by Anthropic focusing on safety and long-context understanding.", category: "AI", rating: 4.7, tags: ["LLM", "Safety", "Research"], url: "https://claude.ai" },
    { id: 4, name: "GitHub Copilot", logo: "https://github.githubassets.com/images/modules/site/features/copilot/copilot-logo.png", description: "AI pair programmer that helps you write code faster with less work.", category: "AI", rating: 4.9, tags: ["Coding", "GitHub", "Autocompletion"], url: "https://github.com/features/copilot" },
    { id: 5, name: "Jasper", logo: "https://www.jasper.ai/favicon.ico", description: "AI content platform that helps teams create high-quality content faster.", category: "AI", rating: 4.5, tags: ["Marketing", "Writing", "Business"], url: "https://jasper.ai" },
    
    // Web Development
    { id: 6, name: "VS Code", logo: "https://upload.wikimedia.org/wikipedia/commons/9/9a/Visual_Studio_Code_1.35_icon.svg", description: "The most popular code editor with extensive plugin ecosystem.", category: "Web Development", rating: 5.0, tags: ["Editor", "Microsoft", "Free"], url: "https://code.visualstudio.com" },
    { id: 7, name: "Next.js", logo: "https://assets.vercel.com/image/upload/v1662130559/nextjs/Icon_light_background.png", description: "The React Framework for the Web, optimized for performance and SEO.", category: "Web Development", rating: 4.8, tags: ["React", "Framework", "Vercel"], url: "https://nextjs.org" },
    { id: 8, name: "Tailwind CSS", logo: "https://upload.wikimedia.org/wikipedia/commons/d/d5/Tailwind_CSS_Logo.svg", description: "A utility-first CSS framework for rapid UI development.", category: "Web Development", rating: 4.9, tags: ["CSS", "Design", "Frontend"], url: "https://tailwindcss.com" },
    { id: 9, name: "Vercel", logo: "https://assets.vercel.com/image/upload/v1588805177/repositories/vercel/logo.png", description: "Platform for frontend developers to deploy and scale instantly.", category: "Web Development", rating: 4.7, tags: ["Hosting", "Deployment", "CI/CD"], url: "https://vercel.com" },
    { id: 10, name: "Figma", logo: "https://upload.wikimedia.org/wikipedia/commons/3/33/Figma-logo.svg", description: "Collaborative interface design tool for teams.", category: "Design", rating: 4.9, tags: ["UI", "UX", "Prototyping"], url: "https://figma.com" },

    // APIs
    { id: 11, name: "Stripe API", logo: "https://upload.wikimedia.org/wikipedia/commons/b/ba/Stripe_Logo%2C_revised_2016.svg", description: "Financial infrastructure for the internet to accept payments.", category: "APIs", rating: 4.9, tags: ["Payments", "Finance", "SDK"], url: "https://stripe.com" },
    { id: 12, name: "Twilio", logo: "https://upload.wikimedia.org/wikipedia/commons/7/7e/Twilio-logo.svg", description: "Communication APIs for SMS, Voice, Video, and Authentication.", category: "APIs", rating: 4.6, tags: ["SMS", "Communication", "Auth"], url: "https://twilio.com" },
    { id: 13, name: "Google Maps API", logo: "https://upload.wikimedia.org/wikipedia/commons/a/aa/Google_Maps_icon_%282020%29.svg", description: "Build real-world map experiences with location data.", category: "APIs", rating: 4.7, tags: ["Maps", "Location", "Google"], url: "https://developers.google.com/maps" },
    { id: 14, name: "Spotify API", logo: "https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg", description: "Access data from the Spotify music catalog and manage user playlists.", category: "APIs", rating: 4.5, tags: ["Music", "Data", "Entertainment"], url: "https://developer.spotify.com" },
    
    // Learning
    { id: 15, name: "freeCodeCamp", logo: "https://upload.wikimedia.org/wikipedia/commons/3/39/FreeCodeCamp_logo.png", description: "Learn to code for free with thousands of tutorials and certifications.", category: "Learning", rating: 5.0, tags: ["Education", "Free", "Certificates"], url: "https://freecodecamp.org" },
    { id: 16, name: "Udemy", logo: "https://upload.wikimedia.org/wikipedia/commons/e/e3/Udemy_logo.svg", description: "Online learning and teaching marketplace with 213,000+ courses.", category: "Learning", rating: 4.4, tags: ["Courses", "Paid", "Skills"], url: "https://udemy.com" },
    { id: 17, name: "Coursera", logo: "https://upload.wikimedia.org/wikipedia/commons/9/97/Coursera-Logo_600x600.svg", description: "Learn without limits with online degrees and certificates.", category: "Learning", rating: 4.6, tags: ["University", "Degrees", "Academic"], url: "https://coursera.org" },
    
    // Mobile
    { id: 18, name: "Flutter", logo: "https://upload.wikimedia.org/wikipedia/commons/1/17/Google-flutter-logo.svg", description: "Google's UI toolkit for building natively compiled applications.", category: "iOS", rating: 4.8, tags: ["Mobile", "Cross-platform", "Google"], url: "https://flutter.dev" },
    { id: 19, name: "React Native", logo: "https://upload.wikimedia.org/wikipedia/commons/a/a7/React-icon.svg", description: "Create native apps for Android and iOS using React.", category: "Android", rating: 4.7, tags: ["Mobile", "React", "Meta"], url: "https://reactnative.dev" },
    
    // DevOps & Cloud
    { id: 20, name: "Docker", logo: "https://upload.wikimedia.org/wikipedia/commons/4/4e/Docker_%28container_engine%29_logo.svg", description: "OS-level virtualization to deliver software in packages called containers.", category: "DevOps", rating: 4.9, tags: ["Containers", "Infrastructure", "Scaling"], url: "https://docker.com" },
    { id: 21, name: "AWS", logo: "https://upload.wikimedia.org/wikipedia/commons/9/93/Amazon_Web_Services_Logo.svg", description: "Comprehensive and broadly adopted cloud platform.", category: "Cloud", rating: 4.8, tags: ["Infrastructure", "Serverless", "Amazon"], url: "https://aws.amazon.com" },
    { id: 22, name: "Terraform", logo: "https://upload.wikimedia.org/wikipedia/commons/0/04/Terraform_Logo.svg", description: "Infrastructure as Code tool for building and changing infrastructure safely.", category: "DevOps", rating: 4.7, tags: ["IaC", "HashiCorp", "Automation"], url: "https://terraform.io" },
    
    // Database
    { id: 23, name: "Supabase", logo: "https://seeklogo.com/images/S/supabase-logo-DCC416CAB2-seeklogo.com.png", description: "The open source Firebase alternative with Postgres.", category: "Database", rating: 4.9, tags: ["Postgres", "Auth", "Realtime"], url: "https://supabase.com" },
    { id: 24, name: "MongoDB", logo: "https://upload.wikimedia.org/wikipedia/commons/9/93/MongoDB_Logo.svg", description: "The most popular NoSQL database for modern applications.", category: "Database", rating: 4.6, tags: ["NoSQL", "JSON", "Cloud"], url: "https://mongodb.com" },
    { id: 25, name: "PlanetScale", logo: "https://planetscale.com/favicon.ico", description: "The world's most advanced serverless MySQL platform.", category: "Database", rating: 4.7, tags: ["MySQL", "Serverless", "Scaling"], url: "https://planetscale.com" },

    // Security
    { id: 26, name: "Auth0", logo: "https://upload.wikimedia.org/wikipedia/commons/a/a2/Auth0_logo.svg", description: "Identity platform for application builders.", category: "Security", rating: 4.5, tags: ["Auth", "Identity", "Okta"], url: "https://auth0.com" },
    { id: 27, name: "Snyk", logo: "https://snyk.io/styleguide/assets/logos/snyk-logo-black.svg", description: "Developer-first security platform for scanning code and dependencies.", category: "Security", rating: 4.6, tags: ["Scanning", "DevSecOps", "Vulnerabilities"], url: "https://snyk.io" },

    // Productivity
    { id: 28, name: "Notion", logo: "https://upload.wikimedia.org/wikipedia/commons/4/45/Notion_app_logo.png", description: "The all-in-one workspace for notes, tasks, and wikis.", category: "Productivity", rating: 4.9, tags: ["Workspace", "Notes", "Collaboration"], url: "https://notion.so" },
    { id: 29, name: "Slack", logo: "https://upload.wikimedia.org/wikipedia/commons/d/d5/Slack_icon_2019.svg", description: "Where work happens - team communication and collaboration.", category: "Productivity", rating: 4.7, tags: ["Chat", "Team", "Business"], url: "https://slack.com" },
    { id: 30, name: "Trello", logo: "https://upload.wikimedia.org/wikipedia/commons/7/7a/Trello-logo-blue.svg", description: "Visual tool for managing projects and organizing anything.", category: "Productivity", rating: 4.5, tags: ["Kanban", "Tasks", "Project"], url: "https://trello.com" }
];

// Generating 70 more dummy items to reach 100+
for (let i = 31; i <= 110; i++) {
    const cats = ["AI", "Web Development", "Android", "iOS", "Backend", "Frontend", "Design", "UI/UX", "APIs", "Database", "Cloud", "DevOps", "Productivity", "Security", "Learning"];
    const cat = cats[i % cats.length];
    toolsData.push({
        id: i,
        name: `${cat} Tool ${i}`,
        logo: `https://picsum.photos/seed/${i}/100/100`,
        description: `This is a high-performance tool for ${cat}. It helps developers streamline their workflow and achieve better results in less time.`,
        category: cat,
        rating: (Math.random() * (5 - 3.5) + 3.5).toFixed(1),
        tags: [cat, "DevTool", "Modern"],
        url: "#"
    });
}
