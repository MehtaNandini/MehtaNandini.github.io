"use client";

import { useEffect, useRef, useState } from "react";
import * as THREE from "three";

const projects = [
  {
    phase: "Ingest",
    title: "Document Classification & Structured Extraction",
    statement: "Turn unstructured documents into records a system can trust.",
    description:
      "A modular document pipeline that moves through OCR, classification, information extraction, and validation—separating each stage so it can be tested, replaced, and scaled independently.",
    input: "Unstructured files",
    output: "Validated records",
    stack: ["Python", "NLP", "Transformers", "OCR", "ETL"],
  },
  {
    phase: "Retrieve",
    title: "RAG-Based LLM Data Pipeline",
    statement: "Make technical knowledge retrievable, traceable, and grounded.",
    description:
      "A retrieval pipeline for scientific content, connecting chunking, metadata, vector search, source grounding, and structured validation into one observable flow.",
    input: "Technical knowledge",
    output: "Grounded answers",
    stack: ["Python", "RAG", "Vector DB", "Metadata", "LLM"],
  },
  {
    phase: "Connect",
    title: "Manufacturing Data Integration & Semantic Search",
    statement: "Connect machines, processes, observations, and meaning.",
    description:
      "A manufacturing knowledge graph that links heterogeneous technical sources through semantic models, mapping, SPARQL queries, and search designed for downstream machine learning.",
    input: "Heterogeneous signals",
    output: "Connected context",
    stack: ["Python", "RDF", "OWL", "SPARQL", "QUDT"],
  },
  {
    phase: "Orchestrate",
    title: "Workflow Automation with LangGraph",
    statement: "Coordinate tools and state without losing control of the result.",
    description:
      "A multi-step workflow system that manages state, routes tool calls, repeats reliable tasks, and validates structured outputs for research and enterprise use cases.",
    input: "Complex task state",
    output: "Validated execution",
    stack: ["Python", "LangGraph", "Tools", "State", "Validation"],
  },
] as const;

const nodePositions = [
  new THREE.Vector3(1.15, 1.75, 0.2),
  new THREE.Vector3(3.25, -1.25, 0.8),
  new THREE.Vector3(1.7, 1.05, -0.2),
  new THREE.Vector3(3.9, -1.45, 0.45),
];

export function ThreeRoadmap() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const sceneRef = useRef<HTMLDivElement>(null);
  const chapterRefs = useRef<Array<HTMLElement | null>>([]);
  const activeRef = useRef(0);
  const [active, setActive] = useState(0);

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
    camera.position.set(0, 0, compact ? 11 : 8.7);

    const world = new THREE.Group();
    world.rotation.set(-0.05, -0.16, -0.04);
    world.scale.setScalar(compact ? 0.82 : 0.9);
    scene.add(world);

    const curve = new THREE.CatmullRomCurve3(nodePositions, false, "catmullrom", 0.4);
    const routeGeometry = new THREE.TubeGeometry(curve, 160, compact ? 0.025 : 0.035, 8, false);
    const routeMaterial = new THREE.MeshBasicMaterial({ color: 0xcaff46 });
    const route = new THREE.Mesh(routeGeometry, routeMaterial);
    world.add(route);

    const shadowCurve = curve.getPoints(160);
    const shadowGeometry = new THREE.BufferGeometry().setFromPoints(shadowCurve);
    const shadowMaterial = new THREE.LineBasicMaterial({ color: 0x375044, transparent: true, opacity: 0.65 });
    const shadowRoute = new THREE.Line(shadowGeometry, shadowMaterial);
    shadowRoute.position.z = -0.16;
    world.add(shadowRoute);

    const nodeGeometry = new THREE.IcosahedronGeometry(compact ? 0.18 : 0.24, 2);
    const ringGeometry = new THREE.TorusGeometry(compact ? 0.42 : 0.52, 0.012, 8, 96);
    const nodes: Array<{ core: THREE.Mesh; ring: THREE.Mesh; material: THREE.MeshStandardMaterial }> = [];

    nodePositions.forEach((position, index) => {
      const group = new THREE.Group();
      group.position.copy(position);

      const material = new THREE.MeshStandardMaterial({
        color: index === 0 ? 0xffa14d : 0xcaff46,
        roughness: 0.3,
        metalness: 0.2,
        emissive: index === 0 ? 0x7b3512 : 0x263d0b,
        emissiveIntensity: index === 0 ? 1.2 : 0.35,
      });
      const core = new THREE.Mesh(nodeGeometry, material);
      const ringMaterial = new THREE.MeshBasicMaterial({
        color: index === 0 ? 0xffa14d : 0x6d897a,
        transparent: true,
        opacity: index === 0 ? 0.9 : 0.36,
      });
      const ring = new THREE.Mesh(ringGeometry, ringMaterial);
      ring.rotation.x = Math.PI / 2.5;
      ring.rotation.y = index * 0.52;
      group.add(core, ring);

      const axisGeometry = new THREE.BufferGeometry().setFromPoints([
        new THREE.Vector3(0, -1.4, 0),
        new THREE.Vector3(0, 1.4, 0),
      ]);
      const axis = new THREE.Line(
        axisGeometry,
        new THREE.LineBasicMaterial({ color: 0x2b4036, transparent: true, opacity: 0.38 }),
      );
      group.add(axis);
      world.add(group);
      nodes.push({ core, ring, material });
    });

    const signalGeometry = new THREE.SphereGeometry(compact ? 0.045 : 0.065, 12, 12);
    const signalMaterial = new THREE.MeshBasicMaterial({ color: 0xffffff });
    const signals = [0, 0.27, 0.54].map((offset) => {
      const signal = new THREE.Mesh(signalGeometry, signalMaterial);
      signal.userData.offset = offset;
      world.add(signal);
      return signal;
    });

    const particleCount = compact ? 170 : 420;
    const particlePositions = new Float32Array(particleCount * 3);
    for (let index = 0; index < particleCount; index += 1) {
      particlePositions[index * 3] = (Math.random() - 0.5) * 16;
      particlePositions[index * 3 + 1] = (Math.random() - 0.5) * 10;
      particlePositions[index * 3 + 2] = (Math.random() - 0.5) * 8 - 1;
    }
    const particlesGeometry = new THREE.BufferGeometry();
    particlesGeometry.setAttribute("position", new THREE.BufferAttribute(particlePositions, 3));
    const particlesMaterial = new THREE.PointsMaterial({
      color: 0x9fb8aa,
      size: compact ? 0.018 : 0.024,
      transparent: true,
      opacity: 0.55,
      sizeAttenuation: true,
    });
    const particles = new THREE.Points(particlesGeometry, particlesMaterial);
    scene.add(particles);

    scene.add(new THREE.AmbientLight(0xc7ddd1, 1.1));
    const keyLight = new THREE.PointLight(0xcaff46, 22, 15);
    keyLight.position.set(1, 3, 5);
    scene.add(keyLight);
    const warmLight = new THREE.PointLight(0xff9f43, 16, 11);
    warmLight.position.set(-4, -2, 4);
    scene.add(warmLight);

    let pointerX = 0;
    let pointerY = 0;
    const onPointerMove = (event: PointerEvent) => {
      pointerX = event.clientX / window.innerWidth - 0.5;
      pointerY = event.clientY / window.innerHeight - 0.5;
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
      world.position.x += ((compact ? -0.15 : 0.4) - nodePositions[current].x * 0.04 - world.position.x) * 0.018;
      world.position.y += (-nodePositions[current].y * 0.05 - world.position.y) * 0.018;
      particles.rotation.y = elapsed * 0.012;

      nodes.forEach(({ core, ring, material }, index) => {
        const selected = index === current;
        const targetScale = selected ? 1.65 : 1;
        core.scale.lerp(new THREE.Vector3(targetScale, targetScale, targetScale), 0.08);
        core.rotation.x += 0.006 + index * 0.001;
        core.rotation.y += 0.009;
        ring.rotation.z += selected ? 0.012 : 0.003;
        ring.scale.lerp(
          new THREE.Vector3(selected ? 1.28 : 1, selected ? 1.28 : 1, selected ? 1.28 : 1),
          0.06,
        );
        material.emissiveIntensity += ((selected ? 1.25 : 0.3) - material.emissiveIntensity) * 0.08;
        (ring.material as THREE.MeshBasicMaterial).opacity +=
          ((selected ? 0.92 : 0.32) - (ring.material as THREE.MeshBasicMaterial).opacity) * 0.08;
      });

      signals.forEach((signal) => {
        const rawProgress = elapsed * 0.075 + Number(signal.userData.offset ?? 0);
        const wrappedProgress = ((rawProgress % 1) + 1) % 1;
        const progress = Number.isFinite(wrappedProgress)
          ? Math.min(0.999999, Math.max(0, wrappedProgress))
          : 0;
        signal.position.copy(curve.getPoint(progress));
      });

      renderer.render(scene, camera);
      if (!reduceMotion) frame = window.requestAnimationFrame(renderFrame);
    };

    renderFrame();

    return () => {
      window.cancelAnimationFrame(frame);
      window.removeEventListener("pointermove", onPointerMove);
      resizeObserver.disconnect();
      routeGeometry.dispose();
      routeMaterial.dispose();
      shadowGeometry.dispose();
      shadowMaterial.dispose();
      nodeGeometry.dispose();
      ringGeometry.dispose();
      signalGeometry.dispose();
      signalMaterial.dispose();
      particlesGeometry.dispose();
      particlesMaterial.dispose();
      timer.dispose();
      nodes.forEach(({ material, ring }) => {
        material.dispose();
        (ring.material as THREE.Material).dispose();
      });
      renderer.dispose();
    };
  }, []);

  return (
    <section className="roadmap-world" id="top">
      <div className="roadmap-scene" ref={sceneRef}>
        <canvas ref={canvasRef} aria-hidden="true" />
        <div className="scene-grid" aria-hidden="true" />
        <div className="scene-hud">
          <p>PROJECT SIGNAL</p>
          <strong>{String(active + 1).padStart(2, "0")} / 04</strong>
          <span>{projects[active].phase}</span>
        </div>
      </div>

      <div className="roadmap-content">
        <div className="roadmap-nav-layer">
          <nav className="scene-dots" aria-label="Project roadmap stations">
            {projects.map((project, index) => (
              <a
                key={project.phase}
                className={index === active ? "active" : ""}
                href={`#project-${index + 1}`}
                aria-label={`Go to project ${index + 1}: ${project.title}`}
                aria-current={index === active ? "step" : undefined}
              >
                <span>{String(index + 1).padStart(2, "0")}</span>
              </a>
            ))}
          </nav>
        </div>
        <section className="hero" aria-labelledby="hero-title">
          <div className="hero-meta">
            <span>Software Engineer</span>
            <span>Based in Germany</span>
          </div>
          <h1 id="hero-title">
            Nandini
            <em>Mehta.</em>
          </h1>
          <p className="hero-copy">
            I design software that transforms complex information into clear, connected, and dependable systems.
          </p>
          <div className="hero-actions">
            <a className="primary-action" href="#roadmap">Enter project roadmap <span aria-hidden="true">↓</span></a>
            <a className="text-action" href="./Nandini_Mehta_CV.pdf" download>Download full CV ↗</a>
          </div>
          <div className="scroll-cue" aria-hidden="true"><span /> Scroll to navigate</div>
        </section>

        <div className="roadmap-intro" id="roadmap">
          <div className="section-label light">
            <span>01</span>
            <p>Project roadmap</p>
          </div>
          <h2>Four projects.<br />One connected trajectory.</h2>
          <p>Each station solves a different part of the same problem: turning complexity into usable software.</p>
        </div>

        <div className="project-chapters">
          {projects.map((project, index) => (
            <article
              className="project-chapter"
              key={project.phase}
              id={`project-${index + 1}`}
              data-step={index}
              ref={(element) => { chapterRefs.current[index] = element; }}
            >
              <div className="chapter-card">
                <div className="chapter-index">
                  <span>{String(index + 1).padStart(2, "0")}</span>
                  <p>{project.phase}</p>
                </div>
                <h3>{project.title}</h3>
                <p className="chapter-statement">{project.statement}</p>
                <p className="chapter-description">{project.description}</p>
                <div className="data-flow" aria-label="Project data flow">
                  <div><span>Input</span><strong>{project.input}</strong></div>
                  <i aria-hidden="true">→</i>
                  <div><span>Output</span><strong>{project.output}</strong></div>
                </div>
                <ul className="chapter-stack" aria-label="Project technologies">
                  {project.stack.map((technology) => <li key={technology}>{technology}</li>)}
                </ul>
              </div>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
