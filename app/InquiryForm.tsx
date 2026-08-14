"use client";

import { useEffect, useRef, useState } from "react";

const inquiryEndpoint = "https://formsubmit.co/nandimehta2204@gmail.com";

export function InquiryForm() {
  const dialogRef = useRef<HTMLDialogElement>(null);
  const [wasSubmitted, setWasSubmitted] = useState(false);

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);

    if (params.get("inquiry") === "sent") {
      const frame = window.requestAnimationFrame(() => {
        setWasSubmitted(true);
        window.history.replaceState(null, "", `${window.location.pathname}${window.location.hash}`);
        if (!dialogRef.current?.open) dialogRef.current?.showModal();
      });

      return () => window.cancelAnimationFrame(frame);
    }
  }, []);

  const openDialog = () => {
    setWasSubmitted(false);
    if (!dialogRef.current?.open) dialogRef.current?.showModal();
  };

  const closeDialog = () => dialogRef.current?.close();

  return (
    <>
      <button
        className="inquiry-trigger"
        type="button"
        aria-haspopup="dialog"
        aria-controls="inquiry-dialog"
        onClick={openDialog}
      >
        Send inquiry
      </button>

      <dialog
        className="inquiry-dialog"
        id="inquiry-dialog"
        ref={dialogRef}
        aria-labelledby="inquiry-title"
      >
        <div className="inquiry-panel">
          <div className="inquiry-heading">
            <div>
              <span>Direct channel</span>
              <h2 id="inquiry-title">Send an inquiry</h2>
            </div>
            <button className="inquiry-close" type="button" onClick={closeDialog} aria-label="Close inquiry form">
              ×
            </button>
          </div>

          {wasSubmitted ? (
            <div className="inquiry-success" role="status">
              <strong>Message sent.</strong>
              <p>Thank you for your inquiry. I will get back to you soon.</p>
              <button type="button" onClick={closeDialog}>Close</button>
            </div>
          ) : (
            <form className="inquiry-form" action={inquiryEndpoint} method="POST">
              <input type="hidden" name="_subject" value="New portfolio inquiry" />
              <input type="hidden" name="_template" value="table" />
              <input type="hidden" name="_next" value="https://mehtanandini.github.io/?inquiry=sent" />
              <input className="inquiry-honeypot" type="text" name="_honey" tabIndex={-1} autoComplete="off" />

              <div className="inquiry-name-fields">
                <label>
                  <span>First name</span>
                  <input type="text" name="First name" autoComplete="given-name" required />
                </label>
                <label>
                  <span>Last name</span>
                  <input type="text" name="Last name" autoComplete="family-name" required />
                </label>
              </div>

              <label>
                <span>Message</span>
                <textarea name="Message" rows={5} required />
              </label>

              <div className="inquiry-form-footer">
                <p>Your message is sent directly to my email.</p>
                <button type="submit">Send message <span aria-hidden="true">↗</span></button>
              </div>
            </form>
          )}
        </div>
      </dialog>
    </>
  );
}
