import { Component, OnInit, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ChatService, Msg } from './chat.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [FormsModule],
  template: `
  <div class="wrap" dir="rtl">
    <header>
      <b>مستشار</b>
      <span>
        <button (click)="showSettings.set(!showSettings())">⚙️</button>
        <button (click)="clear()">🗑️</button>
      </span>
    </header>

    @if (showSettings()) {
      <div class="settings">
        <input [(ngModel)]="apiUrl" placeholder="آدرس بک‌اند" dir="ltr" />
        <input [(ngModel)]="token" placeholder="APP_TOKEN" type="password" dir="ltr" />
        <button (click)="saveSettings()">ذخیره</button>
      </div>
    }

    <main>
      @for (m of messages(); track $index) {
        <div class="msg" [class.me]="m.role === 'user'">{{ m.content }}</div>
      }
      @if (loading()) { <div class="msg">…</div> }
    </main>

    <footer>
      <textarea [(ngModel)]="text" rows="2" placeholder="بنویس..."
                (keydown.enter)="$event.preventDefault(); send()"></textarea>
      <button (click)="send()" [disabled]="loading()">ارسال</button>
    </footer>
  </div>`,
  styles: [`
    .wrap{display:flex;flex-direction:column;height:100dvh;max-width:800px;margin:auto;font-family:system-ui}
    header{display:flex;justify-content:space-between;padding:12px;border-bottom:1px solid #ddd}
    main{flex:1;overflow:auto;padding:12px;display:flex;flex-direction:column;gap:8px}
    .msg{white-space:pre-wrap;padding:10px 14px;border-radius:14px;background:#f1f1f1;max-width:85%}
    .msg.me{background:#d9ecff;align-self:flex-start}
    footer{display:flex;gap:8px;padding:12px;border-top:1px solid #ddd}
    textarea{flex:1;padding:8px;border-radius:8px;border:1px solid #ccc;font:inherit}
    .settings{display:flex;flex-direction:column;gap:6px;padding:12px;background:#fafafa}
  `],
})
export class AppComponent implements OnInit {
  private chat = inject(ChatService);

  messages = signal<Msg[]>([]);
  loading = signal(false);
  showSettings = signal(false);
  text = '';
  apiUrl = this.chat.apiUrl;
  token = this.chat.token;

  async ngOnInit() { this.messages.set(await this.chat.history()); }
  // بقیه بدون تغییر

  saveSettings() {
    this.chat.saveSettings(this.apiUrl, this.token);
    this.showSettings.set(false);
    this.ngOnInit();
  }

  async clear() { await this.chat.clear(); this.messages.set([]); }

  async send() {
    const q = this.text.trim();
    if (!q || this.loading()) return;
    this.text = '';
    this.messages.update(m => [...m, { role: 'user', content: q }, { role: 'assistant', content: '' }]);
    this.loading.set(true);
    try {
      await this.chat.send(q, chunk => this.messages.update(m => {
        const copy = [...m];
        copy[copy.length - 1] = { role: 'assistant', content: copy[copy.length - 1].content + chunk };
        return copy;
      }));
    } catch (e) {
      this.messages.update(m => [...m.slice(0, -1), { role: 'assistant', content: '⚠️ خطا در ارتباط با سرور' }]);
    }
    this.loading.set(false);
  }
}
