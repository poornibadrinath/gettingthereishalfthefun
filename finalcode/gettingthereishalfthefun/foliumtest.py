import folium
from folium import IFrame
from IPython.display import display, HTML

# Create a map centered at Bangalore's coordinates
m = folium.Map(location=[12.9716, 77.5946], zoom_start=12)

# Define cube dimensions
cube_size = 200

# Add an iframe containing the HTML code for 3D cube visualization
html = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>3D Cube</title>
  <style>
    body {{ margin: 0; overflow: hidden; }}
    #cube-container {{ position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%); }}
    canvas {{ display: block; }}
  </style>
</head>
<body>
  <div id="cube-container"></div>
  <script type="module">
    import * as THREE from 'https://cdn.skypack.dev/three@0.132.2/build/three.module.js';

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer();
    renderer.setSize({cube_size}, {cube_size});
    document.getElementById('cube-container').appendChild(renderer.domElement);

    const geometry = new THREE.BoxGeometry(1, 1, 1);
    const material = new THREE.MeshBasicMaterial({{ color: 0x00ff00 }}); // Specify color here (e.g., 0x00ff00 for green)
    const cube = new THREE.Mesh(geometry, material);
    scene.add(cube);

    camera.position.z = 5;

    const animate = () => {{
      requestAnimationFrame(animate);
      cube.rotation.x += 0.01;
      cube.rotation.y += 0.01;
      renderer.render(scene, camera);
    }};
    animate();
  </script>
</body>
</html>
"""

# Create an IFrame with the custom HTML content
iframe = IFrame(html, width=cube_size, height=cube_size)
popup = folium.Popup(iframe, max_width=cube_size)

# Add a marker with the popup containing the 3D cube visualization
marker = folium.Marker(location=[12.9716, 77.5946], popup=popup)
marker.add_to(m)

# Display the map using IPython's display function
display(m)

# Save the map as an HTML file
m.save("3d_cube_map1.html")
