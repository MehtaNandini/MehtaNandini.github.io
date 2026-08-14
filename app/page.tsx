import type { Metadata } from "next";
import type { CSSProperties } from "react";
import { InquiryForm } from "./InquiryForm";
import { ThreeRoadmap } from "./ThreeRoadmap";

export const metadata: Metadata = {
  title: { absolute: "Nandini Mehta | Software Engineer" },
  description:
    "Interactive project roadmap of Nandini Mehta, a software engineer based in Germany.",
};

const capabilities = [
  {
    index: "01",
    title: "Systems",
    detail: "Python · Go · Java · PHP · JavaScript · modular architecture",
  },
  {
    index: "02",
    title: "Data",
    detail: "PostgreSQL · ETL/ELT · validation · time-series · semantic systems",
  },
  {
    index: "03",
    title: "Intelligence",
    detail: "NLP · Transformers · RAG · LangGraph · machine learning",
  },
  {
    index: "04",
    title: "Delivery",
    detail: "Google Cloud · Docker · Kubernetes · CI/CD · observability",
  },
];

const backgroundStars = Array.from({ length: 84 }, (_, index) => {
  const left = ((index * 47 + index * index * 13) % 997) / 9.97;
  const top = ((index * 71 + index * index * 17) % 991) / 9.91;
  const size = index % 13 === 0 ? 2 : index % 5 === 0 ? 1.5 : 1;

  return {
    id: index,
    style: {
      left: `${left}%`,
      top: `${top}%`,
      width: `${size}px`,
      height: `${size}px`,
      animationDelay: `${-(index % 11) * 0.37}s`,
      animationDuration: `${3.4 + (index % 7) * 0.45}s`,
    } as CSSProperties,
  };
});

export default function Home() {
  return (
    <>
      <a className="skip-link" href="#main-content">Skip to content</a>

      <div className="site-starfield" aria-hidden="true">
        {backgroundStars.map((star) => <span key={star.id} style={star.style} />)}
      </div>

      <header className="site-header">
        <a className="brand" href="#top" aria-label="Nandini Mehta — home">
          <span className="brand-core" aria-hidden="true">NM</span>
          <span>Nandini Mehta</span>
        </a>

        <div className="header-actions">
          <nav className="desktop-nav" aria-label="Primary navigation">
            <a href="#roadmap">Roadmap</a>
            <a href="#capabilities">Capabilities</a>
            <a href="#contact">Contact</a>
          </nav>
          <InquiryForm />
        </div>
      </header>

      <main id="main-content">
        <ThreeRoadmap />

        <section className="capabilities-section" id="capabilities" aria-labelledby="capabilities-title">
          <div className="section-label">
            <span>02</span>
            <p>Capability matrix</p>
          </div>
          <div className="capabilities-heading">
            <h2 id="capabilities-title">Built across the full system.</h2>
            <p>
              From raw information to deployed software: the tools change, but the focus stays on clear architecture, traceable data, and dependable outcomes.
            </p>
          </div>
          <div className="capability-grid">
            {capabilities.map((capability) => (
              <article key={capability.index}>
                <span>{capability.index}</span>
                <h3>{capability.title}</h3>
                <p>{capability.detail}</p>
              </article>
            ))}
          </div>
        </section>

      </main>

      <footer className="site-footer" id="contact">
        <div className="footer-primary">
          <p>Software Engineer</p>
          <div className="footer-links">
            <a href="tel:+4917634668019">Mobile: +49 17634668019</a>
            <a href="mailto:nandimehta2204@gmail.com">Email: nandimehta2204@gmail.com</a>
            <a href="https://www.linkedin.com/in/mehtanandini" target="_blank" rel="noreferrer">LinkedIn ↗</a>
            <a href="https://github.com/mehtanandini" target="_blank" rel="noreferrer">GitHub ↗</a>
          </div>
        </div>
        <div className="footer-secondary">
          <p>© {new Date().getFullYear()} Nandini Mehta</p>
          <p>Software Engineer · Germany</p>
          <a href="#top">Return to origin ↑</a>
        </div>
      </footer>
    </>
  );
}
