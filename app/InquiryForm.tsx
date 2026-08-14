"use client";

import { useRef, useState, type FormEvent } from "react";

const emailJsConfig = {
  endpoint: "https://api.emailjs.com/api/v1.0/email/send",
  serviceId: "service_t2csn5s",
  templateId: "template_39i6qtd",
  publicKey: "WwjyfS1fz1MGa4szl",
};
const confirmationMessage =
  "Thank you for your message. Your inquiry was sent successfully. I will contact you as soon as possible.";
const namePattern = "[A-Za-zÀ-ÖØ-öø-ÿĀ-ž'\\- ]{2,50}";

const removeInvalidNameCharacters = (value: string) =>
  value.replace(/[^\p{L}\p{M}' -]/gu, "");

export function InquiryForm() {
  const dialogRef = useRef<HTMLDialogElement>(null);
  const formRef = useRef<HTMLFormElement>(null);
  const [wasSubmitted, setWasSubmitted] = useState(false);
  const [isSending, setIsSending] = useState(false);
  const [submitError, setSubmitError] = useState("");

  const openDialog = () => {
    setWasSubmitted(false);
    setSubmitError("");
    if (!dialogRef.current?.open) dialogRef.current?.showModal();
  };

  const closeDialog = () => dialogRef.current?.close();

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setIsSending(true);
    setSubmitError("");

    const formData = new FormData(event.currentTarget);
    const firstName = String(formData.get("first_name") ?? "").trim();
    const lastName = String(formData.get("last_name") ?? "").trim();
    const email = String(formData.get("email") ?? "").trim();
    const message = String(formData.get("message") ?? "").trim();
    const honeypot = String(formData.get("website") ?? "").trim();

    if (honeypot) {
      setIsSending(false);
      setWasSubmitted(true);
      return;
    }

    try {
      const response = await fetch(emailJsConfig.endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          service_id: emailJsConfig.serviceId,
          template_id: emailJsConfig.templateId,
          user_id: emailJsConfig.publicKey,
          template_params: {
            name: `${firstName} ${lastName}`.trim(),
            email,
            message,
            title: "Portfolio inquiry",
            time: new Intl.DateTimeFormat("en-GB", {
              dateStyle: "medium",
              timeStyle: "short",
              timeZone: "Europe/Berlin",
            }).format(new Date()),
          },
        }),
      });

      if (!response.ok) throw new Error(await response.text());

      formRef.current?.reset();
      setWasSubmitted(true);
    } catch {
      setSubmitError("Your message could not be sent. Please try again or email me directly.");
    } finally {
      setIsSending(false);
    }
  };

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
              <p>{confirmationMessage}</p>
              <button type="button" onClick={closeDialog}>Close</button>
            </div>
          ) : (
            <form className="inquiry-form" ref={formRef} onSubmit={handleSubmit}>
              <input className="inquiry-honeypot" type="text" name="website" tabIndex={-1} autoComplete="off" />

              <div className="inquiry-name-fields">
                <label>
                  <span>First name</span>
                  <input
                    type="text"
                    name="first_name"
                    autoComplete="given-name"
                    pattern={namePattern}
                    minLength={2}
                    maxLength={50}
                    title="Use letters, spaces, apostrophes, or hyphens only."
                    onInput={(event) => {
                      event.currentTarget.value = removeInvalidNameCharacters(event.currentTarget.value);
                    }}
                    required
                  />
                </label>
                <label>
                  <span>Last name</span>
                  <input
                    type="text"
                    name="last_name"
                    autoComplete="family-name"
                    pattern={namePattern}
                    minLength={2}
                    maxLength={50}
                    title="Use letters, spaces, apostrophes, or hyphens only."
                    onInput={(event) => {
                      event.currentTarget.value = removeInvalidNameCharacters(event.currentTarget.value);
                    }}
                    required
                  />
                </label>
              </div>

              <label>
                <span>Email address</span>
                <input
                  type="email"
                  name="email"
                  autoComplete="email"
                  inputMode="email"
                  pattern="[^\s@]+@[^\s@]+\.[^\s@]{2,}"
                  maxLength={254}
                  title="Enter a valid email address, for example name@example.com."
                  required
                />
              </label>

              <label>
                <span>Message</span>
                <textarea name="message" rows={5} required />
              </label>

              {submitError ? (
                <p className="inquiry-error" role="alert">
                  {submitError} <a href="mailto:nandimehta2204@gmail.com">Email Nandini</a>
                </p>
              ) : null}

              <div className="inquiry-form-footer">
                <p>Your message is sent directly to my email.</p>
                <button type="submit" disabled={isSending}>
                  {isSending ? "Sending…" : "Send message"} <span aria-hidden="true">↗</span>
                </button>
              </div>
            </form>
          )}
        </div>
      </dialog>
    </>
  );
}
