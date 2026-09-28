# Get into the Pexip Manager admin page and find a setting

TAGS: pexip, titan
updated: 2026-09-28

source: DVPS-6988 S-06 to S-13 (Adam's click-through, 2026-09-28); DVPS-6798 S-01

What it is: the Pexip Infinity Manager's own admin web page. It is not the AWS console and AWS access does not get you in. It has its own login: Microsoft Entra sign-in (OpenID Connect), with a local account database behind it.

How to reach it:
- The address is a public DNS name under the Titan Pexip domain. It is in Adam's bookmarks, from Cameron, 2026-09-28. It is not written here (D-0031).
- Access to the page is granted by Cameron. Adam has it since 2026-09-28.
- The older path, per Richard: the Titan AVD desktop, then a browser there. Use it if the public name is not reachable.
- Only Adam clicks. The agent asks for a screenshot of one named page and reads it; ids seen in a screenshot are not written down.

Where things are (this install; there is no Gateway rules page):
- Platform > Global settings > Security: OCSP state, OCSP responder URL, SIP TLS certificate verification mode.
- Call control: SIP proxies, H.323 gatekeepers, Microsoft Teams connectors, Policy profiles.
- Users & devices: LDAP sync, administrator authentication.
- System: Syslog servers, Event sinks.
- Nodes keep logs for one day, so an old event has to come from syslog.

Rules of thumb:
- Reading a setting is a human step with the exact menu path in it. Changing one is its own step, and usually its own ticket.
- Check the vendor docs for what a setting covers before clicking through every page: OCSP applies only when SIP TLS verification is on, which made most of one click-through unnecessary.
- What the page talks to over TLS today: one SIP proxy for phone calls, three policy servers, three event sinks on the same three hosts, Entra for admin login, AIMS.
