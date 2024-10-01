// js/main.js
import * as THREE from 'https://cdn.skypack.dev/three@0.128.0';
import { PointerLockControls } from 'https://cdn.skypack.dev/three@0.128.0/examples/jsm/controls/PointerLockControls.js';

let scene, camera, renderer, controls;
const blocks = [];
const blockSize = 1;

// Bewegungskontrollen
const velocity = new THREE.Vector3();
const direction = new THREE.Vector3();
const speed = 5.0;
const keys = {};

const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();

const clock = new THREE.Clock();

function init() {
    // Szene erstellen
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x87ceeb); // Himmelblauer Hintergrund

    // Kamera erstellen
    camera = new THREE.PerspectiveCamera(
        75,
        window.innerWidth / window.innerHeight,
        0.1,
        1000
    );
    camera.position.set(0, 1, 5); // y=1 für näher am Boden

    // Renderer erstellen
    renderer = new THREE.WebGLRenderer({ canvas: document.getElementById('gameCanvas') });
    renderer.setSize(window.innerWidth, window.innerHeight);

    // Licht hinzufügen
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.5);
    directionalLight.position.set(10, 10, 10);
    scene.add(directionalLight);

    // Blöcke hinzufügen
    addInitialBlocks();

    // PointerLockControls initialisieren
    controls = new PointerLockControls(camera, document.body);

    const blocker = document.getElementById('blocker');
    const instructions = document.getElementById('instructions');

    instructions.addEventListener('click', () => {
        controls.lock();
    });

    controls.addEventListener('lock', () => {
        blocker.style.display = 'none';
    });

    controls.addEventListener('unlock', () => {
        blocker.style.display = 'flex';
    });

    scene.add(controls.getObject());

    // Tastatur-Ereignisse
    document.addEventListener('keydown', onKeyDown, false);
    document.addEventListener('keyup', onKeyUp, false);

    // Mausklick-Ereignisse
    document.addEventListener('mousedown', onMouseDown, false);

    // Verhindern des Kontextmenüs beim Rechtsklick
    document.addEventListener('contextmenu', (event) => event.preventDefault());

    // Browser-Resize behandeln
    window.addEventListener('resize', onWindowResize, false);

    animate();
}

function addInitialBlocks() {
    const geometry = new THREE.BoxGeometry(blockSize, blockSize, blockSize);
    for (let x = -10; x <= 10; x++) { // Erweiterte Grundfläche
        for (let z = -10; z <= 10; z++) {
            const material = new THREE.MeshStandardMaterial({ color: getRandomColor() });
            const cube = new THREE.Mesh(geometry, material);
            cube.position.set(x * blockSize, 0, z * blockSize);
            scene.add(cube);
            blocks.push(cube);
        }
    }
}

function getRandomColor() {
    return Math.floor(Math.random() * 16777215);
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

function onKeyDown(event) {
    keys[event.code] = true;
}

function onKeyUp(event) {
    keys[event.code] = false;
}

function onMouseDown(event) {
    if (!controls.isLocked) return;

    // Mausposition für Raycasting setzen (Mittelpunkt des Bildschirms)
    mouse.x = 0;
    mouse.y = 0;

    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObjects(blocks);

    if (intersects.length > 0) {
        const intersect = intersects[0];
        if (event.button === 0) { // Linksklick: Block hinzufügen
            const normal = intersect.face.normal;
            const position = intersect.object.position.clone().addScaledVector(normal, blockSize);
            const geometry = new THREE.BoxGeometry(blockSize, blockSize, blockSize);
            const material = new THREE.MeshStandardMaterial({ color: getRandomColor() });
            const cube = new THREE.Mesh(geometry, material);
            cube.position.copy(position);
            scene.add(cube);
            blocks.push(cube);
        } else if (event.button === 2) { // Rechtsklick: Block entfernen
            scene.remove(intersect.object);
            blocks.splice(blocks.indexOf(intersect.object), 1);
        }
    }
}

function animate() {
    requestAnimationFrame(animate);

    const delta = clock.getDelta();

    // Bewegung aktualisieren
    velocity.x -= velocity.x * 10.0 * delta;
    velocity.z -= velocity.z * 10.0 * delta;

    direction.z = Number(keys['KeyW']) - Number(keys['KeyS']);
    direction.x = Number(keys['KeyD']) - Number(keys['KeyA']);
    direction.normalize();

    if (keys['KeyW'] || keys['KeyS']) velocity.z -= direction.z * speed * delta;
    if (keys['KeyA'] || keys['KeyD']) velocity.x -= direction.x * speed * delta;

    controls.moveRight(-velocity.x * delta);
    controls.moveForward(-velocity.z * delta);

    renderer.render(scene, camera);
}

init();
