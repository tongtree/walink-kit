import { describe, it, expect } from "vitest";
import { createWhatsAppLink, normalizePhone, InvalidPhoneError } from "./index";

describe("normalizePhone", () => {
  it("combines a local number with a country code", () => {
    expect(normalizePhone("13800138000", "86")).toBe("8613800138000");
    expect(normalizePhone("13800138000", "+86")).toBe("8613800138000");
  });

  it("accepts a full international number without duplicating the code", () => {
    expect(normalizePhone("8613800138000", "86")).toBe("8613800138000");
    expect(normalizePhone("+8613800138000")).toBe("8613800138000");
  });

  it("applies the Argentina 549 rule and strips local 15 prefix", () => {
    expect(normalizePhone("1112345678", "54")).toBe("5491112345678");
    expect(normalizePhone("1512345678", "54")).toBe("54912345678");
    expect(normalizePhone("5491112345678", "54")).toBe("5491112345678");
  });

  it("applies the Mexico 521 rule", () => {
    expect(normalizePhone("5512345678", "52")).toBe("5215512345678");
    expect(normalizePhone("5215512345678", "52")).toBe("5215512345678");
  });

  it("throws on empty input", () => {
    expect(() => normalizePhone("", "86")).toThrow(InvalidPhoneError);
    expect(() => normalizePhone("---")).toThrow(InvalidPhoneError);
  });
});

describe("createWhatsAppLink", () => {
  it("builds a wa.me link without a query for an empty message", () => {
    expect(createWhatsAppLink({ phone: "13800138000", countryCode: "86" })).toBe(
      "https://wa.me/8613800138000"
    );
  });

  it("builds a wa.me link with an encoded message", () => {
    expect(
      createWhatsAppLink({ phone: "13800138000", countryCode: "86", message: "hello world" })
    ).toBe("https://wa.me/8613800138000?text=hello%20world");
  });

  it("encodes unicode messages", () => {
    expect(
      createWhatsAppLink({ phone: "13800138000", countryCode: "86", message: "你好" })
    ).toBe("https://wa.me/8613800138000?text=%E4%BD%A0%E5%A5%BD");
  });

  it("supports the api.whatsapp.com variant", () => {
    expect(createWhatsAppLink({ phone: "13800138000", countryCode: "86", variant: "api" })).toBe(
      "https://api.whatsapp.com/send/8613800138000"
    );
  });
});
