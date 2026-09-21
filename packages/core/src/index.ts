/**
 * Error thrown when phone input cannot be normalized into a valid
 * international WhatsApp number.
 */
export class InvalidPhoneError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "InvalidPhoneError";
  }
}

export interface CreateLinkOptions {
  /** Local number, or a full international number (with or without + / leading zeros). */
  phone: string;
  /** Country dial code, e.g. "+86" or "86". Required when `phone` is a local number. */
  countryCode?: string;
  /** Prefilled message text. */
  message?: string;
  /** Link style. Defaults to "wa.me". */
  variant?: "wa.me" | "api";
}

const digitsOnly = (value: string): string => value.replace(/\D/g, "");

const isAllDigits = (value: string): boolean => value.length > 0 && /^\d+$/.test(value);

/**
 * Normalize a phone number into the digits-only international number used by
 * WhatsApp links. Applies the Argentina (54 + 9) and Mexico (52 + 1) rules.
 *
 * @throws {InvalidPhoneError} when no valid number can be produced.
 */
export function normalizePhone(phone: string, countryCode?: string): string {
  const code = digitsOnly(countryCode ?? "");
  let number = digitsOnly(phone);

  if (!number) {
    throw new InvalidPhoneError("Phone number is empty.");
  }

  // Heuristic: a number already carrying a country code.
  const alreadyInternational =
    !countryCode ||
    (code.length > 0 && (number === code || number.startsWith(code))) ||
    number.length >= 11;

  if (alreadyInternational) {
    // Avoid duplicating the dial code if both inputs contain it.
    if (code && number.startsWith(code) && number !== code) {
      // keep as-is
    } else if (code && !number.startsWith(code)) {
      number = `${code}${number}`;
    }
  } else {
    number = `${code}${number}`;
  }

  if (!isAllDigits(number)) {
    throw new InvalidPhoneError("Phone number must contain only digits after normalization.");
  }

  // Argentina: country code 54, insert 9, strip a leading local trunk prefix 15.
  if (number.startsWith("54")) {
    let rest = number.slice(2);
    if (rest.startsWith("15")) {
      rest = rest.slice(2);
    }
    if (!rest.startsWith("9")) {
      rest = `9${rest}`;
    }
    number = `54${rest}`;
  }

  // Mexico: country code 52, insert 1 after the country code.
  if (number.startsWith("52") && !number.startsWith("521")) {
    number = `521${number.slice(2)}`;
  }

  return number;
}

/**
 * Build a WhatsApp click-to-chat link.
 *
 * @throws {InvalidPhoneError} when the phone number is invalid.
 */
export function createWhatsAppLink(options: CreateLinkOptions): string {
  const number = normalizePhone(options.phone, options.countryCode);
  const variant = options.variant ?? "wa.me";
  const base =
    variant === "api"
      ? "https://api.whatsapp.com/send/"
      : "https://wa.me/";

  const message = options.message ?? "";
  const query = message ? `?text=${encodeURIComponent(message)}` : "";

  return `${base}${number}${query}`;
}
