const canvas = document.getElementById('noiseCanvas');
const ctx = canvas.getContext('2d');

let width, height;
let particles = [];
const maxParticles = 300; // Maximum number of particles on screen
const particleColors = ['#52BDE9', '#036CAD', '#52BDE9']; // Particle colors

// Resize canvas and instantly fill the canvas with new particles
function resizeCanvas() {
    width = window.innerWidth;
    height = window.innerHeight;
    canvas.width = width;
    canvas.height = height;

    // Clear existing particles and generate a new set
    particles = []; // Clear existing particles
    for (let i = 0; i < maxParticles; i++) {
        particles.push(createParticle(true)); // Create fully visible particles
    }
}
window.addEventListener('resize', resizeCanvas);
resizeCanvas();

// Generate a new particle
function createParticle(instantVisible = false) {
    return {
        x: Math.random() * width, // Random position across the new canvas
        y: Math.random() * height,
        radius: Math.random() * (Math.min(width, height) * 0.09) + 2, // Scaled with screen size
        alpha: instantVisible ? 1 : 0, // Start fully visible if resizing
        fadeSpeed: Math.random() * 0.004 + 0.001, // Fade speed
        phase: instantVisible ? 'fadeOut' : 'fadeIn', // Start fading out if visible
        color: particleColors[Math.floor(Math.random() * particleColors.length)], // Random color
    };
}

// Update particles: fade in, fade out, and recycle
function updateParticles() {
    particles.forEach(particle => {
        if (particle.phase === 'fadeIn') {
            particle.alpha += particle.fadeSpeed;
            if (particle.alpha >= 1) {
                particle.phase = 'fadeOut';
            }
        } else if (particle.phase === 'fadeOut') {
            particle.alpha -= particle.fadeSpeed;
            if (particle.alpha <= 0) {
                Object.assign(particle, createParticle()); // Recycle particle
            }
        }
    });
}

// Draw particles onto the canvas
function drawParticles() {
    // Set background color
    ctx.fillStyle = '#012C47';
    ctx.fillRect(0, 0, width, height);

    particles.forEach(particle => {
        ctx.beginPath();
        ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(${hexToRgb(particle.color)}, ${particle.alpha})`; // Color with varying opacity
        ctx.fill();
    });
}

// Convert HEX to RGB
function hexToRgb(hex) {
    const bigint = parseInt(hex.slice(1), 16);
    const r = (bigint >> 16) & 255;
    const g = (bigint >> 8) & 255;
    const b = bigint & 255;
    return `${r}, ${g}, ${b}`;
}

// Animation loop
function animate() {
    updateParticles();
    drawParticles();
    requestAnimationFrame(animate);
}

// Start animation
animate();
