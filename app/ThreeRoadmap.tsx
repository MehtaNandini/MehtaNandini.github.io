"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import * as THREE from "three";
import { ProjectChapterCard, ProjectDetailDialog } from "./ProjectDetails";
import { projects } from "./projectData";

const nodePositions = [
  new THREE.Vector3(1.3, 2.95, 0.15),
  new THREE.Vector3(3.35, 1.72, -0.35),
  new THREE.Vector3(1.45, 0.5, 0.05),
  new THREE.Vector3(3.5, -0.72, 0.4),
  new THREE.Vector3(1.3, -1.94, -0.2),
  new THREE.Vector3(3.6, -3.16, 0.15),
];

function createProjectTexture(project: (typeof projects)[number], index: number) {
  const surface = document.createElement("canvas");
  surface.width = 1024;
  surface.height = 640;
  const context = surface.getContext("2d");
  if (!context) throw new Error("Canvas 2D context is unavailable");

  context.fillStyle = "#0b1712";
  context.fillRect(0, 0, surface.width, surface.height);

  context.fillStyle = "#caff46";
  context.fillRect(0, 0, surface.width, 8);
  context.font = "600 38px monospace";
  context.fillText(String(index + 1).padStart(2, "0"), 64, 82);

  context.fillStyle = "#91a39a";
  context.textAlign = "right";
  context.font = "600 28px monospace";
  context.fillText(project.phase.toUpperCase(), 960, 78);
  context.textAlign = "left";

  const words = project.shortTitle.split(" ");
  const lines: string[] = [];
  let line = "";
  context.font = "600 68px Arial";
  words.forEach((word) => {
    const candidate = line ? `${line} ${word}` : word;
    if (context.measureText(candidate).width > 860 && line) {
      lines.push(line);
      line = word;
    } else {
      line = candidate;
    }
  });
  if (line) lines.push(line);

  context.fillStyle = "#e9f0eb";
  lines.slice(0, 3).forEach((text, lineIndex) => {
    context.fillText(text, 64, 210 + lineIndex * 72);
  });

  context.strokeStyle = "rgba(233, 240, 235, 0.25)";
  context.beginPath();
  context.moveTo(64, 470);
  context.lineTo(960, 470);
  context.stroke();

  context.fillStyle = "#91a39a";
  context.font = "500 24px monospace";
  context.fillText("INPUT", 64, 522);
  context.fillText("OUTPUT", 620, 522);
  context.fillStyle = "#e9f0eb";
  context.font = "600 28px Arial";
  context.fillText(project.input, 64, 568);
  context.fillText(project.output, 620, 568);
  context.fillStyle = "#ff9f43";
  context.font = "600 34px Arial";
  context.fillText("→", 510, 565);

  const texture = new THREE.CanvasTexture(surface);
  texture.colorSpace = THREE.SRGBColorSpace;
  texture.needsUpdate = true;
  return texture;
}

export function ThreeRoadmap() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const sceneRef = useRef<HTMLDivElement>(null);
  const chapterRefs = useRef<Array<HTMLElement | null>>([]);
  const activeRef = useRef(0);
  const [active, setActive] = useState(0);
  const [focusedProject, setFocusedProject] = useState<number | null>(null);
  const [selectedProject, setSelectedProject] = useState<number | null>(null);
  const closeProject = useCallback(() => setSelectedProject(null), []);

  const focusProjectCard = useCallback((projectIndex: number, behavior: ScrollBehavior = "smooth") => {
    const target = chapterRefs.current[projectIndex];
    if (!target) return;

    activeRef.current = projectIndex;
    setActive(projectIndex);
    setFocusedProject(projectIndex);
    target.querySelector<HTMLElement>(".chapter-card")?.focus({ preventScroll: true });
    target.scrollIntoView({ behavior, block: "center", inline: "nearest" });
    window.history.replaceState(null, "", `#project-${projectIndex + 1}`);
  }, []);

  useEffect(() => {
    const match = window.location.hash.match(/^#project-(\d+)$/);
    const projectIndex = match ? Number(match[1]) - 1 : -1;
    if (projectIndex < 0 || projectIndex >= projects.length) return;

    const frame = window.requestAnimationFrame(() => focusProjectCard(projectIndex, "auto"));
    return () => window.cancelAnimationFrame(frame);
  }, [focusProjectCard]);

  useEffect(() => {
    const chapters = chapterRefs.current.filter(Boolean) as HTMLElement[];
    const observer = new IntersectionObserver(
      (entries) => {
        const visible = entries
          .filter((entry) => entry.isIntersecting)
          .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];

        if (!visible) return;
        const next = Number((visible.target as HTMLElement).dataset.step ?? 0);
        activeRef.current = next;
        setActive(next);
      },
      { threshold: [0.3, 0.55, 0.75], rootMargin: "-12% 0px -22%" },
    );

    chapters.forEach((chapter) => observer.observe(chapter));
    return () => observer.disconnect();
  }, []);

  useEffect(() => {
    const canvas = canvasRef.current;
    const container = sceneRef.current;
    if (!canvas || !container) return;

    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const compact = window.innerWidth < 760;
    let renderer: THREE.WebGLRenderer;

    try {
      renderer = new THREE.WebGLRenderer({
        canvas,
        alpha: true,
        antialias: !compact,
        powerPreference: "high-performance",
      });
    } catch {
      container.classList.add("webgl-fallback");
      return;
    }

    renderer.setPixelRatio(Math.min(window.devicePixelRatio, compact ? 1.25 : 1.75));
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.setClearColor(0x07100d, 0);

    const scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x07100d, 0.055);

    const camera = new THREE.PerspectiveCamera(42, 1, 0.1, 100);
    camera.position.set(0, 0, compact ? 13.3 : 10.2);

    const world = new THREE.Group();
    world.rotation.set(-0.05, -0.16, -0.04);
    world.scale.setScalar(compact ? 0.58 : 0.68);
    scene.add(world);

    const cardWidth = compact ? 2.05 : 2.4;
    const cardHeight = compact ? 1.28 : 1.5;
    const cardGeometry = new THREE.PlaneGeometry(cardWidth, cardHeight);
    const cardHitGeometry = new THREE.PlaneGeometry(cardWidth + 0.38, cardHeight + 0.3);
    const cardFrameGeometry = new THREE.EdgesGeometry(cardGeometry);
    const cardBackGeometry = new THREE.BoxGeometry(cardWidth, cardHeight, 0.06);
    const portGeometry = new THREE.BoxGeometry(0.11, 0.11, 0.08);
    const cardHitMaterial = new THREE.MeshBasicMaterial({
      transparent: true,
      opacity: 0,
      side: THREE.DoubleSide,
      depthWrite: false,
    });
    const cardRotations = [
      new THREE.Euler(-0.04, -0.18, -0.035),
      new THREE.Euler(0.04, 0.16, 0.045),
      new THREE.Euler(-0.03, -0.13, -0.025),
      new THREE.Euler(0.035, 0.12, 0.035),
      new THREE.Euler(-0.025, -0.15, -0.03),
      new THREE.Euler(0.03, 0.14, 0.03),
    ];
    const cardFaces: THREE.Mesh[] = [];
    const cards: Array<{
      group: THREE.Group;
      material: THREE.MeshBasicMaterial;
      frameMaterial: THREE.LineBasicMaterial;
      backMaterial: THREE.MeshBasicMaterial;
      portMaterial: THREE.MeshBasicMaterial;
      texture: THREE.CanvasTexture;
      basePosition: THREE.Vector3;
      baseRotation: THREE.Euler;
    }> = [];

    nodePositions.forEach((position, index) => {
      const group = new THREE.Group();
      group.position.copy(position);
      group.rotation.copy(cardRotations[index]);

      const texture = createProjectTexture(projects[index], index);
      texture.anisotropy = renderer.capabilities.getMaxAnisotropy();
      const material = new THREE.MeshBasicMaterial({
        map: texture,
        transparent: true,
        opacity: index === 0 ? 1 : 0.58,
        side: THREE.DoubleSide,
      });
      const face = new THREE.Mesh(cardGeometry, material);
      face.position.z = 0.045;
      face.userData.projectIndex = index;

      const hitArea = new THREE.Mesh(cardHitGeometry, cardHitMaterial);
      hitArea.position.z = 0.09;
      hitArea.userData.projectIndex = index;
      cardFaces.push(hitArea);

      const frameMaterial = new THREE.LineBasicMaterial({
        color: 0xcaff46,
        transparent: true,
        opacity: index === 0 ? 0.95 : 0.28,
      });
      const frame = new THREE.LineSegments(cardFrameGeometry, frameMaterial);
      frame.position.z = 0.075;

      const backMaterial = new THREE.MeshBasicMaterial({
        color: 0x07100d,
        transparent: true,
        opacity: 0.9,
      });
      const backing = new THREE.Mesh(cardBackGeometry, backMaterial);

      const portMaterial = new THREE.MeshBasicMaterial({
        color: index === 0 ? 0xff9f43 : 0xcaff46,
        transparent: true,
        opacity: index === 0 ? 1 : 0.6,
      });
      const inputPort = new THREE.Mesh(portGeometry, portMaterial);
      inputPort.position.set(-cardWidth / 2 - 0.055, 0, 0.08);
      const outputPort = new THREE.Mesh(portGeometry, portMaterial);
      outputPort.position.set(cardWidth / 2 + 0.055, 0, 0.08);

      group.add(backing, face, frame, inputPort, outputPort, hitArea);
      world.add(group);
      cards.push({
        group,
        material,
        frameMaterial,
        backMaterial,
        portMaterial,
        texture,
        basePosition: position.clone(),
        baseRotation: cardRotations[index].clone(),
      });
    });

    let pointerX = 0;
    let pointerY = 0;
    let hoveredProject: number | null = null;
    const raycaster = new THREE.Raycaster();
    const pointer = new THREE.Vector2();

    const projectAtPointer = (event: PointerEvent) => {
      const bounds = canvas.getBoundingClientRect();
      pointer.set(
        ((event.clientX - bounds.left) / bounds.width) * 2 - 1,
        -((event.clientY - bounds.top) / bounds.height) * 2 + 1,
      );
      raycaster.setFromCamera(pointer, camera);
      const intersection = raycaster.intersectObjects(cardFaces, false)[0];
      return typeof intersection?.object.userData.projectIndex === "number"
        ? Number(intersection.object.userData.projectIndex)
        : null;
    };

    const onPointerMove = (event: PointerEvent) => {
      pointerX = event.clientX / window.innerWidth - 0.5;
      pointerY = event.clientY / window.innerHeight - 0.5;
    };
    const onCanvasPointerMove = (event: PointerEvent) => {
      hoveredProject = projectAtPointer(event);
      canvas.style.cursor = hoveredProject === null ? "default" : "pointer";
    };
    const onCanvasPointerLeave = () => {
      hoveredProject = null;
      canvas.style.cursor = "default";
    };
    const onCanvasClick = (event: PointerEvent) => {
      const projectIndex = projectAtPointer(event);
      if (projectIndex === null) return;

      focusProjectCard(projectIndex, reduceMotion ? "auto" : "smooth");
    };

    const resize = () => {
      const { width, height } = container.getBoundingClientRect();
      renderer.setSize(width, height, false);
      camera.aspect = width / Math.max(height, 1);
      camera.updateProjectionMatrix();
    };

    const resizeObserver = new ResizeObserver(resize);
    resizeObserver.observe(container);
    window.addEventListener("pointermove", onPointerMove, { passive: true });
    canvas.addEventListener("pointermove", onCanvasPointerMove, { passive: true });
    canvas.addEventListener("pointerleave", onCanvasPointerLeave);
    canvas.addEventListener("click", onCanvasClick);
    resize();

    const timer = new THREE.Timer();
    timer.connect(document);
    let frame = 0;
    const renderFrame = () => {
      timer.update();
      const elapsed = timer.getElapsed();
      const current = activeRef.current;

      world.rotation.y += ((compact ? -0.05 : -0.12) + pointerX * 0.12 - world.rotation.y) * 0.025;
      world.rotation.x += (-pointerY * 0.08 - world.rotation.x) * 0.025;
      world.position.x += ((compact ? -0.05 : 0.28) - nodePositions[current].x * 0.025 - world.position.x) * 0.018;
      world.position.y += (-nodePositions[current].y * 0.05 - world.position.y) * 0.018;
      cards.forEach(({ group, material, frameMaterial, portMaterial, basePosition, baseRotation }, index) => {
        const selected = index === current;
        const hovered = index === hoveredProject;
        const targetScale = hovered ? (selected ? 1.2 : 1.08) : selected ? 1.12 : 0.9;
        group.scale.lerp(new THREE.Vector3(targetScale, targetScale, targetScale), 0.07);
        group.position.y = basePosition.y + Math.sin(elapsed * 0.55 + index * 1.3) * 0.045;
        group.position.z += (basePosition.z + (hovered ? 0.28 : 0) - group.position.z) * 0.12;
        group.rotation.x +=
          (baseRotation.x - pointerY * 0.035 - group.rotation.x) * 0.035;
        group.rotation.y +=
          (baseRotation.y + pointerX * 0.05 + Math.sin(elapsed * 0.35 + index) * 0.018 + (hovered ? -0.055 : 0) - group.rotation.y) * 0.055;
        group.rotation.z = baseRotation.z + Math.sin(elapsed * 0.42 + index) * 0.008;
        material.opacity += ((selected || hovered ? 1 : 0.58) - material.opacity) * 0.1;
        frameMaterial.opacity += ((selected || hovered ? 0.95 : 0.28) - frameMaterial.opacity) * 0.1;
        portMaterial.opacity += ((selected || hovered ? 1 : 0.6) - portMaterial.opacity) * 0.1;
      });

      renderer.render(scene, camera);
      if (!reduceMotion) frame = window.requestAnimationFrame(renderFrame);
    };

    renderFrame();

    return () => {
      window.cancelAnimationFrame(frame);
      window.removeEventListener("pointermove", onPointerMove);
      canvas.removeEventListener("pointermove", onCanvasPointerMove);
      canvas.removeEventListener("pointerleave", onCanvasPointerLeave);
      canvas.removeEventListener("click", onCanvasClick);
      resizeObserver.disconnect();
      cardGeometry.dispose();
      cardHitGeometry.dispose();
      cardHitMaterial.dispose();
      cardFrameGeometry.dispose();
      cardBackGeometry.dispose();
      portGeometry.dispose();
      timer.dispose();
      cards.forEach(({ material, frameMaterial, backMaterial, portMaterial, texture }) => {
        material.dispose();
        frameMaterial.dispose();
        backMaterial.dispose();
        portMaterial.dispose();
        texture.dispose();
      });
      renderer.dispose();
    };
  }, [focusProjectCard]);

  return (
    <section className="roadmap-world" id="top">
      <div className="roadmap-scene" ref={sceneRef}>
        <canvas ref={canvasRef} aria-hidden="true" />
        <div className="scene-hud">
          <p>PROJECT INDEX</p>
          <strong>{String(active + 1).padStart(2, "0")} / {String(projects.length).padStart(2, "0")}</strong>
          <span>{projects[active].phase}</span>
        </div>
      </div>

      <div className="roadmap-content">
        <section className="hero" aria-labelledby="hero-title">
          <div className="hero-meta">
            <span>Software Engineer</span>
            <span>Based in Germany</span>
          </div>
          <h1 id="hero-title">
            Nandini
            <em>Mehta.</em>
          </h1>
          <div className="hero-actions">
            <a className="primary-action" href="#roadmap">Enter project roadmap <span aria-hidden="true">↓</span></a>
            <a className="text-action" href="./Nandini_Mehta_CV.pdf" download>Download full CV ↗</a>
          </div>
          <div className="scroll-cue" aria-hidden="true"><span /> Scroll to navigate</div>
        </section>

        <section className="project-chapters" id="roadmap" aria-label="Project portfolio">
          {projects.map((project, index) => (
            <article
              className={`project-chapter${focusedProject === index ? " is-focused" : ""}`}
              key={project.phase}
              id={`project-${index + 1}`}
              data-step={index}
              ref={(element) => { chapterRefs.current[index] = element; }}
            >
              <ProjectChapterCard project={project} index={index} onOpen={setSelectedProject} />
            </article>
          ))}
        </section>
      </div>
      {selectedProject !== null && (
        <ProjectDetailDialog
          index={selectedProject}
          project={projects[selectedProject]}
          onClose={closeProject}
        />
      )}
    </section>
  );
}
