# VaR Cult Moves to Matrix: Why We Left Discord

*The internet used to be protocols. Then it became platforms. Matrix is bringing protocols back.*

**Published: 2026-04-07 | TyphooN | MarketWizardry.org**

> **DISCLAIMER:** This is not financial advice. This is a rant about communication infrastructure. The opinions expressed are those of someone who ran an IRC server before most Discord users were born.

---

## Discord Is Dead to Us

The VaR Cult Discord server has been discontinued. Not because we ran out of things to say — we never do — but because Discord decided that age verification via government ID scanning is an acceptable requirement for running a community server. It isn't.

Let me be clear about what happened: Discord started requiring server owners and moderators to submit government-issued identification. A platform that started as a gaming chat app now wants your driver's license. A company that stores messages on servers you don't control, in a jurisdiction you didn't choose, with encryption you can't verify, now also wants a copy of your face attached to your real name in their database.

No.

The VaR Cult does not hand government identification to corporations in exchange for the privilege of running a chat room. We ran trading discussions on Discord. We shared market analysis. We debated VaR strategies. None of that requires a Fortune 500 company to know our legal names and birth dates. None of that requires a centralized platform at all.

So we left.

---

## How Did We Get Here?

The internet was built on protocols. Email is a protocol (SMTP). The web is a protocol (HTTP). Usenet was a protocol (NNTP). IRC was a protocol (IRC). FTP is a protocol. DNS is a protocol. Every foundational internet service was designed as an open standard that anyone could implement, anyone could host, and no single entity controlled.

Then something happened. Slowly, over two decades, protocols were replaced by platforms.

- **Email** survived (barely) but Gmail handles 1.8 billion accounts. Google reads your email. You agreed to it in the ToS you didn't read.
- **Usenet** died. Reddit replaced it. Reddit is a company that went public and now optimizes for advertiser engagement, not discussion quality.
- **IRC** died. Discord replaced it. Discord is a company valued at $15 billion that stores every message you've ever sent on their servers, forever.
- **Blogs** died. Twitter/X replaced them. A billionaire now decides what you see in your feed.
- **Forums** died. Facebook Groups replaced them. Your group admin doesn't control the algorithm. Zuckerberg does.

Every protocol was replaced by a platform. Every platform is controlled by a corporation. Every corporation eventually enshittifies — raises prices, adds surveillance, removes features, demands identification, sells data, or goes bankrupt and takes your community with it.

This is not a conspiracy theory. This is the documented history of every major internet platform over the past 20 years. The pattern is always the same:

1. **Launch**: Free, open, developer-friendly. "We're not like the others."
2. **Growth**: Attract users. Become the default. Kill the protocol you replaced.
3. **Monetize**: Ads. Premium tiers. API paywalls. Data harvesting.
4. **Enshittify**: Remove features. Require ID. Algorithmic feeds. Hostile to third-party clients.
5. **Lock-in**: By this point, your community has no alternative. The protocol is dead. You're trapped.

Discord is at stage 4. The age verification requirement is enshittification. The platform you chose because it was "free and easy" now wants your passport.

---

## What Discord Actually Is

Discord is not a communication tool. Discord is a data collection platform that happens to have chat features.

Every message you send is stored on Discord's servers. Not your servers. Discord's. You don't own it. You can't export it. You can't self-host it. You can't verify the encryption. You can't audit the code. You can't control who has access to your data.

When you type a message in Discord, it travels from your device to Discord's servers (AWS infrastructure), gets stored in their database, gets indexed for search, gets analyzed for "safety" by their automated systems, and then gets delivered to the recipient. At every step, Discord has full access to the plaintext content of your message.

This is not private communication. This is posting on someone else's computer and hoping they don't read it. Hope is not a security model.

The moment Discord decided to require government ID, they made the implicit explicit: **you are not the customer. You are the product. And now they want to attach a government-verified identity to the product.**

---

## IRC Did It Right (In 1988)

IRC — Internet Relay Chat — was created in 1988. It is a protocol, not a platform. Anyone can run an IRC server. Anyone can connect. No company controls the network. No corporation stores your messages. No algorithm decides what you see.

IRC had:
- **Self-hosted servers** — you controlled the hardware, the logs, the access
- **Decentralized networks** — if one server went down, others continued
- **No message persistence** — messages existed in transit and then vanished (unless you chose to log them locally)
- **No identity requirements** — pick a nickname, connect, talk
- **Open protocol** — any client could connect, anyone could build a server

IRC's weakness was UX. No inline images. No message history on reconnect. No mobile push notifications. No voice channels. The protocol was powerful but the user experience was 1988.

Discord saw this gap and filled it with a beautiful UI, voice chat, screen sharing, emoji reactions, and file uploads — all running on a centralized, proprietary, surveillance-capable platform that you don't control.

The trade was: give up sovereignty for convenience. Most people took the trade without understanding the terms.

---

## Matrix: IRC for 2026

Matrix is the answer. It is what IRC would be if IRC were designed today with modern requirements but the same philosophical commitment to open protocols and user sovereignty.

**Matrix is a protocol, not a platform.** Like email, anyone can run a Matrix server. Like IRC, anyone can connect. Like HTTP, the protocol is an open standard. Unlike Discord, no single company controls the network.

What Matrix offers:
- **Self-hosted servers** — run your own Synapse/Dendrite/Conduit server on your own hardware
- **Federated network** — servers talk to each other like email servers do. A user on matrix.org can message a user on your personal server.
- **End-to-end encryption** — Megolm protocol. Verified. Audited. Not "trust us, it's encrypted" — actually encrypted, client-side, with verifiable keys.
- **Message history** — unlike IRC, messages persist (on your server, that you control)
- **No identity requirements** — create an account with a username. No phone number. No government ID. No driver's license scan.
- **Open protocol** — any client can connect. Element, FluffyChat, Nheko, Cinny, gomuks — pick the one you like.
- **Bridges** — connect to IRC, Slack, Telegram, Signal, even Discord from within Matrix. One client for everything.

Matrix is not perfect. The reference server (Synapse) is resource-heavy. Federation can be slow. The ecosystem is younger than Discord's. But the architecture is right. The philosophy is right. The protocol is open. The encryption is real. Nobody is going to ask you for your passport.

---

## The VaR Cult Matrix Space

The VaR Cult now operates on Matrix. Contact `@TyphooN-:matrix.org` for an invite to the VaR Cult Matrix Space.

**Recommended client: [FluffyChat](https://fluffychat.im)** — clean UI, E2EE by default, cross-platform (Android, iOS, Linux, macOS, Windows, web).

You can also reach TyphooN on [X/Twitter (@MarketW1zardry)](https://x.com/MarketW1zardry) to coordinate a Matrix invite.

**Why Matrix over Discord:**
- No government ID requirement
- No corporate surveillance of trading discussions
- End-to-end encrypted by default
- Self-hostable — we control the server, the data, and the access
- Open protocol — if matrix.org disappears tomorrow, the protocol continues
- No algorithmic feed — you see what was posted, in order, without a corporation deciding what's "relevant"

**Why FluffyChat:**
- E2EE enabled by default (no configuration needed)
- Clean, modern UI — closest to Discord's UX without Discord's surveillance
- Available everywhere (mobile, desktop, web)
- Open source

The VaR Cult didn't leave Discord because Discord is bad software. Discord is excellent software. We left because Discord is a corporation that decided our government identification is a reasonable price for running a chat room. It isn't. The software is good. The company's trajectory is not. The protocol is the product. The platform is temporary.

---

## The Lesson

Every time you build a community on a platform you don't control, you are renting. The landlord can raise the rent. The landlord can change the rules. The landlord can ask for your ID. The landlord can evict you.

Protocols are property. Platforms are leases. IRC was property. Discord is a lease. Matrix is property again.

The VaR Cult trades on Darwinex, where we control the algorithm. We chart on TyphooN-Terminal, where we control the source code. And now we communicate on Matrix, where we control the server.

**Sovereignty is not optional. It is the entire point.**

Contact `@TyphooN-:matrix.org` on Matrix. Recommended client: [FluffyChat](https://fluffychat.im). Or reach out on [X/Twitter](https://x.com/MarketW1zardry).

-- TyphooN

---

> **DISCLAIMER:** This post expresses opinions about communication platforms. The author is not affiliated with Matrix.org Foundation, Element, FluffyChat, Discord Inc., or any platform mentioned. Matrix is an open protocol maintained by the Matrix.org Foundation. Discord is a trademark of Discord Inc. The author's opinions on data sovereignty and corporate surveillance are exactly that — opinions formed after decades of watching open protocols get replaced by closed platforms.
