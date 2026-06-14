import bs4
from bs4 import BeautifulSoup

def main():
    with open('travel_spots.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # 1. Update <head> with fonts and new styles
    head = soup.find('head')
    
    # Add Google Fonts if not there
    fonts_link = soup.new_tag('link', href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&family=Shippori+Mincho:wght@500;700&display=swap", rel="stylesheet")
    head.append(fonts_link)
    
    # Replace style tag
    old_style = soup.find('style')
    if old_style:
        old_style.decompose()
        
    new_style = soup.new_tag('style')
    new_style.string = """
    body {
        font-family: 'Noto Sans JP', sans-serif;
        margin: 0;
        padding: 20px;
        color: #2c3e50;
        background: url('https://images.pexels.com/photos/31658696/pexels-photo-31658696.jpeg') no-repeat center center fixed;
        background-size: cover;
    }
    body::before {
        content: "";
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(6px);
        -webkit-backdrop-filter: blur(6px);
        z-index: -1;
    }

    .table-container {
        max-width: 1200px;
        margin: 0 auto;
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 16px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.5);
    }

    .header {
        background: linear-gradient(135deg, rgba(26,34,71,0.95) 0%, rgba(43,59,108,0.95) 100%);
        color: #ffffff;
        padding: 24px;
        font-size: 2rem;
        font-family: 'Shippori Mincho', serif;
        text-align: center;
        letter-spacing: 2px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        border-bottom: 2px solid rgba(255, 183, 197, 0.5);
    }

    table {
        width: 100%;
        border-collapse: collapse;
    }

    th, td {
        padding: 16px;
        text-align: left;
        border-bottom: 1px solid rgba(0,0,0,0.05);
    }

    th {
        background-color: rgba(248, 249, 250, 0.6);
        color: #1A2247;
        font-weight: 700;
        text-transform: uppercase;
        font-size: 0.85rem;
        letter-spacing: 1px;
    }

    td {
        font-size: 0.95rem;
        line-height: 1.6;
        vertical-align: top;
    }

    a {
        color: #d84361;
        text-decoration: none;
        font-weight: 700;
        transition: color 0.3s;
    }

    a:hover {
        color: #1A2247;
        text-decoration: underline;
    }

    /* Glassmorphism Rows & Hover Animations */
    .main-row {
        cursor: pointer;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        background: transparent;
        opacity: 0; /* For scroll reveal */
        transform: translateY(20px);
    }

    .main-row.visible {
        opacity: 1;
        transform: translateY(0);
    }

    .main-row:hover {
        background: rgba(255, 183, 197, 0.25) !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(255, 183, 197, 0.4);
    }

    .details-row {
        background-color: transparent;
    }

    .details-row.hidden {
        display: none;
    }

    .expanded-card {
        padding: 20px;
        margin: 12px 16px;
        background: rgba(255, 255, 255, 0.95);
        border-left: 6px solid #d84361;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-radius: 8px;
        animation: slideDown 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }

    @keyframes slideDown {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .expanded-card h4 {
        margin-top: 0;
        color: #1A2247;
        font-size: 1.3rem;
        margin-bottom: 12px;
        font-family: 'Shippori Mincho', serif;
    }

    .expanded-card p {
        margin-bottom: 10px;
        line-height: 1.6;
        color: #444;
    }

    /* Mobile Responsive Cards */
    @media (max-width: 768px) {
        body { padding: 10px; }
        .table-container { background: transparent; box-shadow: none; border: none; backdrop-filter: none; }
        .header { border-radius: 16px; margin-bottom: 15px; }
        table, thead, tbody, th, td, tr { display: block; }
        thead tr { display: none; }
        .main-row {
            margin-bottom: 15px;
            background: rgba(255, 255, 255, 0.9) !important;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            padding: 5px;
            border: 1px solid rgba(255,183,197,0.3);
        }
        td {
            border: none;
            padding: 8px 15px;
            position: relative;
        }
        td::before {
            content: attr(data-label);
            font-weight: 700;
            color: #d84361;
            display: block;
            font-size: 0.75rem;
            text-transform: uppercase;
            margin-bottom: 4px;
            letter-spacing: 1px;
        }
        .expanded-card { margin: 0 0 15px 0; }
    }

    /* Sakura Canvas */
    #sakura-canvas {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 9999;
    }
    """
    head.append(new_style)
    
    # 2. Add data-label to all td elements based on th headers
    headers = [th.get_text(strip=True) for th in soup.find_all('th')]
    
    for row in soup.find_all('tr', class_='main-row'):
        cells = row.find_all('td')
        for i, cell in enumerate(cells):
            if i < len(headers):
                cell['data-label'] = headers[i]
                
    # 3. Add canvas and JS to bottom of body
    body = soup.find('body')
    
    # Remove existing sakura canvas if present
    existing_canvas = soup.find('canvas', id='sakura-canvas')
    if existing_canvas:
        existing_canvas.decompose()
        
    canvas = soup.new_tag('canvas', id='sakura-canvas')
    body.append(canvas)
    
    # We will just append the script
    script = soup.new_tag('script')
    script.string = """
    // Sakura falling effect
    const canvas = document.getElementById('sakura-canvas');
    const ctx = canvas.getContext('2d');
    let width = canvas.width = window.innerWidth;
    let height = canvas.height = window.innerHeight;
    const petals = [];
    const petalCount = 60; // Reduce for mobile performance if needed

    window.addEventListener('resize', () => {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
    });

    class Petal {
        constructor() {
            this.x = Math.random() * width;
            this.y = Math.random() * height - height;
            this.w = 10 + Math.random() * 15;
            this.h = 10 + Math.random() * 15;
            this.opacity = this.w / 25;
            this.speedX = 1 + Math.random() * 2;
            this.speedY = 1 + Math.random() * 2;
            this.rotation = Math.random() * 360;
            this.rotationSpeed = (Math.random() - 0.5) * 5;
        }
        draw() {
            ctx.save();
            ctx.translate(this.x, this.y);
            ctx.rotate(this.rotation * Math.PI / 180);
            ctx.globalAlpha = this.opacity;
            ctx.fillStyle = '#ffb7c5';
            ctx.beginPath();
            // Draw a basic petal shape
            ctx.moveTo(0, 0);
            ctx.bezierCurveTo(this.w/2, -this.h/2, this.w, 0, 0, this.h);
            ctx.bezierCurveTo(-this.w, 0, -this.w/2, -this.h/2, 0, 0);
            ctx.fill();
            ctx.restore();
        }
        update() {
            this.y += this.speedY;
            this.x += this.speedX;
            this.rotation += this.rotationSpeed;
            if (this.y > height + this.h) {
                this.y = -this.h;
                this.x = Math.random() * width;
            }
            if (this.x > width + this.w) {
                this.x = -this.w;
            }
        }
    }

    for (let i = 0; i < petalCount; i++) {
        petals.push(new Petal());
    }

    function animateSakura() {
        ctx.clearRect(0, 0, width, height);
        for (let i = 0; i < petals.length; i++) {
            petals[i].update();
            petals[i].draw();
        }
        requestAnimationFrame(animateSakura);
    }
    animateSakura();

    // Intersection Observer for smooth scroll-reveal
    document.addEventListener("DOMContentLoaded", () => {
        const rows = document.querySelectorAll('.main-row');
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    // Stop observing once visible to keep it shown
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1, rootMargin: "0px 0px -50px 0px" });

        rows.forEach(row => observer.observe(row));
    });
    """
    body.append(script)
    
    with open('travel_spots.html', 'w', encoding='utf-8') as f:
        f.write(str(soup))
        
if __name__ == "__main__":
    main()
