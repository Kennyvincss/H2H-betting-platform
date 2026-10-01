# NeatSpace demo video — narration script

Female voice (Kokoro TTS, voice `af_heart`), 1920×1080, 2:58 total. Subtitles are burned in; `neatspace-demo.srt` is the same text as a separate file.

**Intro** — Meet NeatSpace, a home cleaning platform for Lagos, Nigeria. Customers pick a service, choose a time, and book in minutes, while the owner runs the whole business from one dashboard.

**Home** — The home page shows the rating, homes cleaned, and the next open slot. It explains the three steps to book, lists every service, and introduces your dedicated cleaner.

**Services** — On the Services page, every cleaning is priced upfront. Standard, Deep, Move In or Move Out, and Custom cleans each show a starting price, the estimated duration, and exactly what's included.

**How** — How it works walks through the process, then explains confirmations, reminders, live status tracking, and the deposit and cancellation policy.

**Reviews Referrals** — The Reviews page collects honest feedback from real homes, and the referral program gives five thousand naira to both you and a friend.

**Book A** — To book, customers sign in or create a free account. The booking wizard starts with the home: type, bedrooms, bathrooms, condition, and pets. Next, they build the cleaning with a service and add-ons, and the price updates live.

**Book B** — They can upload room photos, enter the address and service area to see any travel fee, then choose from time slots the cleaner can genuinely work.

**Book C** — Finally, they add contact details, how often they'd like a cleaning, and an optional promo code, then review everything and pay a secure deposit.

**Account** — Every booking gets its own page, where customers track its status, reschedule, pay the balance, and leave a review. The footer links to the rescheduling, terms, privacy, and refund policies.

**Owner Overview** — Now the owner side. After signing in, the Overview gives a daily summary: today's bookings and revenue, upcoming jobs, pending payments, ratings, and follow-ups.

**Owner Bookings** — Bookings lists every job, filtered by status. Opening one shows the customer, the home details, payments, and the timeline, so the owner can move the job forward.

**Owner Calendar** — The calendar shows the day, week, or month at a glance, and the owner can block off time when they're unavailable.

**Owner Customers** — Customers tracks every client, their spending and preferences, with one-click reminders for follow-ups and unpaid bookings.

**Owner Payments** — Payments shows collected deposits, outstanding balances, refunds, and scheduled revenue.

**Owner Analytics** — Analytics charts revenue over time, highlights insights like the busiest day and top service, and breaks down capacity, services, and add-ons.

**Owner Reviews Notif** — Reviews and issues gathers ratings and problems to resolve, and Notifications logs every new booking and payment.

**Owner Settings** — In Settings, the owner controls the business profile, working hours, deposit, fees, cancellation policy, services, add-ons, service areas, and promo codes. Changes go live immediately.

**Outro** — NeatSpace. A cleaner home, without the hassle.

## Rebuilding

1. Run the NeatSpace app locally on `http://127.0.0.1:8080`.
2. `E=<owner email> P=<password> node pipeline/record.mjs` records one clip per scene (credentials are read from env vars, never stored).
3. Generate the voice clips into `vo/`, then `python3 pipeline/assemble.py` trims, syncs and writes the SRT.
