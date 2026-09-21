<script setup lang="ts">
import { ref } from "vue";
import QRCode from "qrcode";
import { createWhatsAppLink, InvalidPhoneError } from "@walink/core";

const COUNTRIES: { code: string; dial: string }[] = [
  { code: "US", dial: "+1" },
  { code: "GB", dial: "+44" },
  { code: "IN", dial: "+91" },
  { code: "ID", dial: "+62" },
  { code: "BR", dial: "+55" },
  { code: "MX", dial: "+52" },
  { code: "DE", dial: "+49" },
  { code: "ES", dial: "+34" },
  { code: "AR", dial: "+54" },
  { code: "CN", dial: "+86" },
];

const dial = ref("+1");
const phone = ref("");
const message = ref("");
const link = ref("");
const copied = ref(false);
const error = ref("");
const qrDataUrl = ref("");

const generate = async () => {
  error.value = "";
  link.value = "";
  qrDataUrl.value = "";
  try {
    link.value = createWhatsAppLink({
      phone: phone.value,
      countryCode: dial.value,
      message: message.value,
    });
    qrDataUrl.value = await QRCode.toDataURL(link.value, { width: 240 });
  } catch (err) {
    if (err instanceof InvalidPhoneError) {
      error.value = err.message;
    } else {
      throw err;
    }
  }
};

const copy = async () => {
  await navigator.clipboard.writeText(link.value);
  copied.value = true;
  window.setTimeout(() => {
    copied.value = false;
  }, 2000);
};

const downloadQr = () => {
  const anchor = document.createElement("a");
  anchor.href = qrDataUrl.value;
  anchor.download = "whatsapp-qr-code.png";
  anchor.click();
};
</script>

<template>
  <main class="wrap">
    <span class="badge">Open source · MIT</span>
    <h1>WhatsApp Link Generator</h1>
    <p class="sub">Create a click-to-chat link and QR code for any WhatsApp number.</p>

    <div class="card">
      <label for="phone">Phone number</label>
      <div class="row">
        <select v-model="dial" id="dial">
          <option v-for="country in COUNTRIES" :key="country.code" :value="country.dial">
            {{ country.code }} {{ country.dial }}
          </option>
        </select>
        <input v-model="phone" id="phone" type="tel" inputmode="numeric" placeholder="123 456 7890" />
      </div>

      <label for="message">Prefilled message <span style="font-weight: 400">(optional)</span></label>
      <textarea v-model="message" id="message" placeholder="Hello, I found you on..."></textarea>

      <p v-if="error" class="error">{{ error }}</p>

      <button type="button" @click="generate">Generate link</button>

      <div v-if="link" class="result">
        <div class="link-box">
          <input :value="link" readonly />
          <button type="button" @click="copy">{{ copied ? "Copied!" : "Copy" }}</button>
        </div>
        <div class="qr">
          <img v-if="qrDataUrl" :src="qrDataUrl" alt="WhatsApp QR code" width="240" height="240" />
          <button type="button" @click="downloadQr">Download QR code</button>
        </div>
      </div>
    </div>

    <footer>
      Powered by <a href="https://walink.wadesk.io" target="_blank" rel="noopener">WALink</a> ·
      <a href="https://link.wadesk.io" target="_blank" rel="noopener">Generador · Español / Português</a>
    </footer>
  </main>
</template>
