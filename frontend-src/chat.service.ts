import { Injectable } from '@angular/core';

export interface Msg { role: 'user' | 'assistant'; content: string; }

@Injectable({ providedIn: 'root' })
export class ChatService {
  // آدرس بک‌اند (روی گوشی: آدرس Tailscale کامپیوتر، مثلاً http://100.x.y.z:8000)
  apiUrl = localStorage.getItem('apiUrl') ?? 'http://localhost:8000';
  token = localStorage.getItem('token') ?? '';

  saveSettings(apiUrl: string, token: string) {
    this.apiUrl = apiUrl; this.token = token;
    localStorage.setItem('apiUrl', apiUrl);
    localStorage.setItem('token', token);
  }

  private headers() {
    return { 'Content-Type': 'application/json', Authorization: `Bearer ${this.token}` };
  }

  async history(): Promise<Msg[]> {
    const r = await fetch(`${this.apiUrl}/api/history`, { headers: this.headers() });
    return r.ok ? r.json() : [];
  }

  async clear() {
    await fetch(`${this.apiUrl}/api/history`, { method: 'DELETE', headers: this.headers() });
  }

  // جواب کلمه‌به‌کلمه می‌رسد و onChunk صدا زده می‌شود
  async send(message: string, onChunk: (t: string) => void) {
    const r = await fetch(`${this.apiUrl}/api/chat`, {
      method: 'POST', headers: this.headers(), body: JSON.stringify({ message }),
    });
    if (!r.ok || !r.body) throw new Error(`HTTP ${r.status}`);
    const reader = r.body.getReader();
    const dec = new TextDecoder();
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      onChunk(dec.decode(value, { stream: true }));
    }
  }
}
