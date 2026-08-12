"use client";

/* eslint-disable @next/next/no-img-element */

import type { CSSProperties, KeyboardEvent } from "react";
import { useCallback, useEffect, useRef, useState } from "react";
import type { PortfolioProject } from "./projectData";

type ProjectChapterCardProps = {
  index: number;
  project: PortfolioProject;
  onOpen: (index: number) => void;
};

export function ProjectChapterCard({ index, project, onOpen }: ProjectChapterCardProps) {
  const [flipAngle, setFlipAngle] = useState(0);
  const [flipSpeed, setFlipSpeed] = useState(0);
  const [isFlipping, setIsFlipping] = useState(false);
  const timersRef = useRef<number[]>([]);

  useEffect(
    () => () => {
      timersRef.current.forEach((timer) => window.clearTimeout(timer));
    },
    [],
  );

  const revealProject = () => {
    if (isFlipping) return;

    const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (prefersReducedMotion) {
      onOpen(index);
      return;
    }

    setIsFlipping(true);
    const speed = 180;
    setFlipSpeed(speed);
    setFlipAngle(360);

    const revealTimer = window.setTimeout(() => {
      onOpen(index);
      setIsFlipping(false);
      setFlipSpeed(0);
      setFlipAngle(0);
      timersRef.current = [];
    }, speed + 20);
    timersRef.current.push(revealTimer);
  };

  const onKeyDown = (event: KeyboardEvent<HTMLDivElement>) => {
    if (event.key !== "Enter" && event.key !== " ") return;
    event.preventDefault();
    revealProject();
  };

  const flipStyle = {
    "--flip-angle": `${flipAngle}deg`,
    "--flip-speed": `${flipSpeed}ms`,
  } as CSSProperties;

  return (
    <div className="chapter-card-shell">
      <div
        className={`chapter-card${isFlipping ? " is-flipping" : ""}`}
        style={flipStyle}
        role="button"
        tabIndex={0}
        aria-haspopup="dialog"
        aria-label={`Open complete project details for ${project.title}`}
        onClick={revealProject}
        onKeyDown={onKeyDown}
      >
        <div className="chapter-index">
          <span>{String(index + 1).padStart(2, "0")}</span>
          <p>{project.phase}</p>
        </div>
        <h3>{project.title}</h3>
        <p className="chapter-technology-label">Languages / Technologies</p>
        <ul className="chapter-stack" aria-label="Project technologies">
          {project.stack.map((technology) => <li key={technology}>{technology}</li>)}
        </ul>
      </div>
    </div>
  );
}

type ProjectDetailDialogProps = {
  index: number;
  project: PortfolioProject;
  onClose: () => void;
};

export function ProjectDetailDialog({ index, project, onClose }: ProjectDetailDialogProps) {
  const [activeShot, setActiveShot] = useState(0);
  const [autoAdvance, setAutoAdvance] = useState(true);
  const closeButtonRef = useRef<HTMLButtonElement>(null);
  const inactivityTimerRef = useRef<number | null>(null);

  const registerInteraction = useCallback(() => {
    setAutoAdvance(false);
    if (inactivityTimerRef.current !== null) {
      window.clearTimeout(inactivityTimerRef.current);
    }
    inactivityTimerRef.current = window.setTimeout(() => {
      setAutoAdvance(true);
      inactivityTimerRef.current = null;
    }, 60_000);
  }, []);

  useEffect(() => {
    closeButtonRef.current?.focus();
  }, []);

  useEffect(
    () => () => {
      if (inactivityTimerRef.current !== null) {
        window.clearTimeout(inactivityTimerRef.current);
      }
    },
    [],
  );

  useEffect(() => {
    const onKeyDown = (event: globalThis.KeyboardEvent) => {
      if (event.key === "Escape") onClose();
    };

    const root = document.documentElement;
    const body = document.body;
    const lockedScrollY = window.scrollY;
    const previousRootOverflow = root.style.overflow;
    const previousRootOverscroll = root.style.overscrollBehavior;
    const previousRootScrollBehavior = root.style.scrollBehavior;
    const previousBodyOverflow = body.style.overflow;
    const previousBodyPosition = body.style.position;
    const previousBodyTop = body.style.top;
    const previousBodyWidth = body.style.width;

    root.style.overflow = "hidden";
    root.style.overscrollBehavior = "none";
    body.style.overflow = "hidden";
    body.style.position = "fixed";
    body.style.top = `-${lockedScrollY}px`;
    body.style.width = "100%";
    window.addEventListener("keydown", onKeyDown);

    return () => {
      window.removeEventListener("keydown", onKeyDown);
      body.style.overflow = previousBodyOverflow;
      body.style.position = previousBodyPosition;
      body.style.top = previousBodyTop;
      body.style.width = previousBodyWidth;
      root.style.scrollBehavior = "auto";
      window.scrollTo(0, lockedScrollY);
      root.style.overflow = previousRootOverflow;
      root.style.overscrollBehavior = previousRootOverscroll;
      root.style.scrollBehavior = previousRootScrollBehavior;
    };
  }, [onClose]);

  useEffect(() => {
    if (project.screenshots.length < 2) return;
    if (!autoAdvance) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const timer = window.setInterval(() => {
      setActiveShot((current) => (current + 1) % project.screenshots.length);
    }, 5200);
    return () => window.clearInterval(timer);
  }, [autoAdvance, project]);

  const changeShot = (direction: number) => {
    setActiveShot((current) =>
      (current + direction + project.screenshots.length) % project.screenshots.length,
    );
  };

  const activeScreenshot = project.screenshots[activeShot];
  return (
    <div
      className="project-detail-layer"
      onPointerMove={registerInteraction}
      onPointerDown={registerInteraction}
      onWheel={registerInteraction}
      onKeyDownCapture={registerInteraction}
      onTouchStart={registerInteraction}
    >
      <section
        className="project-detail-dialog"
        role="dialog"
        aria-modal="true"
        aria-labelledby="project-detail-title"
      >
        <header className="project-detail-header">
          <div>
            <span>CASE STUDY {String(index + 1).padStart(2, "0")} / 06</span>
            <p>{project.phase} · {project.status}</p>
          </div>
          <button ref={closeButtonRef} className="project-detail-close" type="button" onClick={onClose}>
            Close <span aria-hidden="true">×</span>
          </button>
        </header>

        <div className="project-detail-hero">
          <div>
            <h2 id="project-detail-title">{project.title}</h2>
            <p className="project-detail-statement">{project.statement}</p>
          </div>
          <p>{project.description}</p>
        </div>

        <div className="project-media-block">
          <div className="project-media-stage" key={activeScreenshot.src}>
            <div className="project-media-viewport">
              <img
                src={activeScreenshot.src}
                alt={activeScreenshot.alt}
                decoding="sync"
                fetchPriority="high"
                draggable={false}
              />
            </div>
            <div className="project-media-overlay">
              <span>{String(activeShot + 1).padStart(2, "0")} / {String(project.screenshots.length).padStart(2, "0")}</span>
              <p>{activeScreenshot.caption}</p>
            </div>
            <div className="project-media-controls" aria-label="Screenshot controls">
              <a
                className="project-open-image"
                href={activeScreenshot.src}
                target="_blank"
                rel="noreferrer"
                aria-label={`Open full-size image: ${activeScreenshot.caption}`}
              >
                <span className="project-open-image-icon" aria-hidden="true">
                  <i /><i /><i /><i />
                </span>
              </a>
              {project.screenshots.length > 1 && (
                <>
                  <button type="button" onClick={() => changeShot(-1)} aria-label="Previous screenshot">←</button>
                  <button type="button" onClick={() => changeShot(1)} aria-label="Next screenshot">→</button>
                </>
              )}
            </div>
          </div>
          <div className="project-media-strip" aria-label="Project screenshots">
            {project.screenshots.map((screenshot, screenshotIndex) => (
              <button
                type="button"
                className={screenshotIndex === activeShot ? "active" : ""}
                key={screenshot.src}
                onClick={() => setActiveShot(screenshotIndex)}
                aria-label={`Show screenshot ${screenshotIndex + 1}: ${screenshot.caption}`}
                aria-current={screenshotIndex === activeShot ? "true" : undefined}
              >
                <img src={screenshot.src} alt="" loading="lazy" />
                <span>{String(screenshotIndex + 1).padStart(2, "0")}</span>
              </button>
            ))}
          </div>
        </div>

        <div className="project-detail-sections">
          <section>
            <div className="detail-section-label"><span>01</span><p>What&apos;s included</p></div>
            <ul className="detail-feature-list">
              {project.features.map((feature) => <li key={feature}>{feature}</li>)}
            </ul>
          </section>
          <section>
            <div className="detail-section-label"><span>02</span><p>Still in development</p></div>
            <ul className="detail-feature-list future">
              {project.future.map((item) => <li key={item}>{item}</li>)}
            </ul>
          </section>
        </div>

        <section className="project-technology-section">
          <div className="detail-section-label"><span>03</span><p>Languages and technology</p></div>
          <ul>
            {project.technologies.map((technology) => <li key={technology}>{technology}</li>)}
          </ul>
        </section>
      </section>

    </div>
  );
}
