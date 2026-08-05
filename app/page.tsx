import type { Metadata } from "next";
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

export default function Home() {
  return (
    <>
      <a className="skip-link" href="#main-content">Skip to content</a>

      <header className="site-header">
        <a className="brand" href="#top" aria-label="Nandini Mehta — home">
          <span className="brand-core" aria-hidden="true">NM</span>
          <span>Nandini Mehta</span>
        </a>

        <nav className="desktop-nav" aria-label="Primary navigation">
          <a href="#roadmap">Roadmap</a>
          <a href="#capabilities">Capabilities</a>
          <a href="#contact">Contact</a>
        </nav>

        <a className="header-cv" href="./Nandini_Mehta_CV.pdf" download>
          Download CV <span aria-hidden="true">↗</span>
        </a>
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

        <section className="contact-section" id="contact" aria-labelledby="contact-title">
          <div className="contact-orbit" aria-hidden="true">
            <span>OPEN CHANNEL</span>
          </div>
          <p className="contact-kicker">Based in Germany · Working internationally</p>
          <h2 id="contact-title">Have a complex problem?</h2>
          <a className="contact-link" href="mailto:nandimehta2204@gmail.com">
            Let&apos;s map it out. <span aria-hidden="true">↗</span>
          </a>
          <div className="contact-footer">
            <p>Software Engineer</p>
            <div>
              <a href="https://www.linkedin.com/in/mehtanandini" target="_blank" rel="noreferrer">LinkedIn ↗</a>
              <a href="https://github.com/mehtanandini" target="_blank" rel="noreferrer">GitHub ↗</a>
              <a href="./Nandini_Mehta_CV.pdf" download>Full CV ↓</a>
            </div>
          </div>
        </section>
      </main>

      <footer>
        <p>© {new Date().getFullYear()} Nandini Mehta</p>
        <p>Software Engineer · Germany</p>
        <a href="#top">Return to origin ↑</a>
      </footer>
    </>
  );
}
