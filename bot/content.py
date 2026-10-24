"""Content bank for IMADI Tech (American English).

Each format has its own list. The bot cycles through each list in order, so with the
full schedule (5 posts, 4 carousels, 4 reels a week) nothing repeats for about three
weeks. Add more entries anywhere in a list to stretch that out; no other change needed.

Writing rules used here:
- Only facts IMADI Tech can stand behind (project details as stated on imadi.tech).
  No invented statistics, prices or guarantees.
- In headlines, *words in asterisks* get the brand gradient.
- Captions don't include the WhatsApp line or hashtags: the bot adds them per platform.

Layouts
  post:     chat | statement | mythfact | case | checklist
  carousel: list of slides, each cover | list | text | cta
  reel:     scenes, each {headline, sub?}, with one voiceover line per scene
"""

HASHTAG_SETS = [
    "#WhatsAppAutomation #SmallBusiness #KarachiBusiness #LeadGeneration #AIChatbot",
    "#BusinessAutomation #WhatsAppBusiness #CustomerExperience #PakistanBusiness #SalesTips",
    "#AIForBusiness #LeadManagement #DubaiBusiness #Entrepreneurs #Automation",
    "#Chatbot #InstagramAutomation #SMB #DigitalTransformation #IMADITech",
]

POSTS = [
    {
        "layout": "chat", "tag": "Lead tip",
        "chat": [("in", "Hi, what's the price for an L-shaped kitchen?", "Sent 10:47 PM"),
                 ("out", "Hi! Thanks for reaching out 😊", "Replied 11:02 AM, next day")],
        "headline": "By then, they'd already *bought elsewhere.*",
        "lead": "An AI assistant answers every inquiry in seconds, day or night.",
        "caption": ("Your customer messaged at 10:47 PM. You replied at 11:02 AM. By then, they'd already bought from someone else.\n\n"
                    "Most businesses don't lose leads because of bad ads. They lose them because nobody answered in time.\n\n"
                    "IMADI Tech builds AI assistants for WhatsApp and Instagram that reply in seconds, share your designs and prices, send quotes, and follow up automatically."),
    },
    {
        "layout": "statement", "tag": "Reality check",
        "headline": "More ad spend won't fix *slow replies.*",
        "lead": "If inquiries wait hours for an answer, a bigger budget just means more people waiting.",
        "caption": ("Before you raise your ad budget, check one thing: how fast does your team reply?\n\n"
                    "When messages sit unanswered, more ads only bring more people who never hear back. Fix the response first, then scale the ads.\n\n"
                    "We set up WhatsApp and Instagram assistants that answer every inquiry instantly, so the leads you already pay for actually turn into conversations."),
    },
    {
        "layout": "mythfact", "tag": "Myth vs fact", "headline": "Chatbots sound *robotic?*",
        "myth": "A chatbot will sound robotic and annoy my customers.",
        "fact": "A good assistant answers the simple questions fast, then hands serious buyers to your team, with the full chat attached.",
        "caption": ("Myth: chatbots annoy customers.\n\nFact: what annoys customers is waiting. A well-built assistant answers the common questions in seconds (prices, sizes, delivery, timings) and passes the conversation to a real person the moment a customer is ready to buy.\n\n"
                    "Your team spends its time on serious buyers. Customers get answers when they ask."),
    },
    {
        "layout": "case", "tag": "Client story", "client": "ALICO Enterprises · Karachi", "headline": "2 hours a day, down to *20 minutes*",
        "problem": "Staff spent about 2 hours every day in Excel on quotations, invoices, stock and payments.",
        "solution": "One app that does it all, works offline and shares documents on WhatsApp. The same work now takes about 20 minutes.",
        "caption": ("From 2 hours a day to about 20 minutes.\n\n"
                    "ALICO Enterprises, a general order supplier in Karachi, was running quotations, invoices, stock and payments through spreadsheets. We built them one business app that handles all of it, works even when the internet drops, and shares print-ready documents on WhatsApp.\n\n"
                    "If your team is buried in repetitive admin, there's probably a faster way."),
    },
    {
        "layout": "checklist", "tag": "Quick audit",
        "headline": "Is your business *losing leads?*",
        "items": ["Messages after 8 PM wait until morning", "Nobody follows up after sending a quote", "Leads live on different salespeople's phones"],
        "caption": ("A 10-second audit for your business:\n\n"
                    "• Do messages after 8 PM wait until morning?\n• Does anyone follow up after sending a quote?\n• Can you see every lead in one place?\n\n"
                    "If you answered yes, no, no, you're paying for leads that quietly slip away. That's exactly what WhatsApp automation fixes."),
    },
    {
        "layout": "statement", "tag": "Follow-up",
        "headline": "The sale usually happens *after the quote.*",
        "lead": "Most buyers don't decide on the first message. A timely follow-up brings them back.",
        "caption": ("Sending the quote isn't the finish line. It's where most deals are actually won or lost.\n\n"
                    "Buyers compare, get busy, and forget. A friendly follow-up the next day, and another a few days later, keeps you in the conversation.\n\n"
                    "Our assistants send those follow-ups automatically, so no quote is ever left hanging."),
    },
    {
        "layout": "case", "tag": "Client story", "client": "Multi-branch business · Nairobi", "headline": "See *every lead* your team gets",
        "problem": "Some salespeople were taking WhatsApp leads, selling outside the company and keeping the commission.",
        "solution": "Each branch connects its WhatsApp to one dashboard, so management sees every lead and conversation.",
        "caption": ("What happens to your leads after they reach your sales team?\n\n"
                    "A multi-branch business in Nairobi found out some leads were being diverted. We built Company Monitor: each branch links its WhatsApp Business number with a QR code, and management sees every lead, every conversation and every reply time in one dashboard.\n\n"
                    "Visibility protects revenue."),
    },
    {
        "layout": "chat", "tag": "How it works",
        "chat": [("in", "Do you deliver to DHA? And what sizes do you have?", "11:20 PM"),
                 ("out", "Yes, we deliver across Karachi! Here are our sizes and prices 👇", "11:20 PM, instantly")],
        "headline": "Every question answered, *even at midnight.*",
        "lead": "Your assistant shares prices, sizes and designs from a sheet you update yourself.",
        "caption": ("Your customers don't shop on your schedule. They message late at night, on weekends, during Friday prayers.\n\n"
                    "An AI assistant on your WhatsApp answers the questions you get every day (delivery areas, sizes, prices, designs) instantly, using a price sheet you can update yourself."),
    },
    {
        "layout": "mythfact", "tag": "Myth vs fact", "headline": "Only for *big companies?*",
        "myth": "Automation is only for big companies.",
        "fact": "Small, owner-led businesses benefit most: one assistant can handle the first reply for every lead.",
        "caption": ("Myth: automation is only for big companies with big budgets.\n\nFact: small businesses often feel the difference most. When the owner is also the salesperson, every missed message is a missed sale.\n\n"
                    "One WhatsApp assistant can handle first replies, common questions and follow-ups for every lead, without hiring another person."),
    },
    {
        "layout": "checklist", "tag": "What you get",
        "headline": "One assistant, *five jobs done.*",
        "items": ["Instant replies on WhatsApp", "Prices and designs shared automatically", "Quotes sent as PDFs", "Follow-ups for quiet leads", "Every lead in one dashboard"],
        "caption": ("What does a WhatsApp lead assistant actually do?\n\n"
                    "1. Replies to every inquiry instantly\n2. Shares your prices and designs\n3. Sends quotes as PDF documents\n4. Follows up with people who go quiet\n5. Shows every lead and its status in one dashboard\n\n"
                    "All on the WhatsApp number your customers already use."),
    },
    {
        "layout": "case", "tag": "Client story", "client": "Logistics company · United Kingdom", "headline": "Claims handled *on WhatsApp*",
        "problem": "Staff had to dig through emails to find and handle damage claims.",
        "solution": "A WhatsApp bot now runs the claims process, and staff approve or reject claims from one dashboard.",
        "caption": ("Automation isn't only for sales. It's for any process that runs on messages.\n\n"
                    "For a logistics company in the UK, damage claims were scattered across email. We built a WhatsApp bot that collects every claim properly, and a dashboard where staff raise, approve or reject them. Less searching, nothing lost, all data in sync."),
    },
    {
        "layout": "statement", "tag": "Speed matters",
        "headline": "Customers message *three shops.* They buy from the first to reply.",
        "lead": "Speed is the easiest competitive edge you can have.",
        "caption": ("Here's how most buyers shop today: they find three businesses, send the same message to all of them, and go with whoever answers first and clearly.\n\n"
                    "You don't need the lowest price to win that race. You need the fastest helpful reply."),
    },
    {
        "layout": "case", "tag": "Client story", "client": "Scrap collection business · Karachi", "headline": "No app. *Just WhatsApp.*",
        "problem": "Pickups depended on informal calls, with no record of requests, prices or collections.",
        "solution": "Customers and collectors handle everything in a WhatsApp chat, and every pickup reaches a dashboard.",
        "caption": ("No app to download. No forms. Just WhatsApp.\n\n"
                    "For ReNaz, a scrap collection business in Karachi, we built a platform where customers book pickups and collectors complete jobs entirely through WhatsApp conversations, while the team tracks every pickup on a dashboard.\n\n"
                    "Your customers are already on WhatsApp. Your business can be too."),
    },
    {
        "layout": "chat", "tag": "Follow-up",
        "chat": [("out", "Hi Sara! Just checking if you had any questions about the quote we sent yesterday 😊", "Automatic follow-up"),
                 ("in", "Yes! Can we do it in walnut instead?", "Reply 4 min later")],
        "headline": "One friendly nudge *restarts the sale.*",
        "lead": "Automatic follow-ups bring quiet leads back without anyone having to remember.",
        "caption": ("Quiet doesn't mean not interested. Usually it just means busy.\n\n"
                    "A short, friendly follow-up the day after a quote is often all it takes to restart the conversation. Our assistants send them automatically, at the right time, in your brand's tone."),
    },
]

CAROUSELS = [
    {
        "slides": [
            {"layout": "cover", "num": "5", "headline": "reasons your ads bring messages, *not sales*", "lead": "Swipe to see where leads slip away →"},
            {"layout": "list", "headline": "Where leads get lost", "items": ["Late replies: buyers go with whoever answers first", "No follow-up after the quote", "Leads spread across salespeople's phones"]},
            {"layout": "list", "headline": "And two more", "items": ["Prices and designs shared slowly, one chat at a time", "No one can see which leads were won or lost"]},
            {"layout": "cta", "headline": "Reply instantly. Send quotes. *Follow up automatically.*", "lead": "See it working for your business in a free 10-minute demo."},
        ],
        "caption": "5 reasons your ads bring messages but not sales, and how to fix every one of them. Save this for your next team meeting.",
    },
    {
        "slides": [
            {"layout": "cover", "headline": "How a WhatsApp lead assistant *works*", "lead": "From first message to closed deal, step by step →"},
            {"layout": "text", "headline": "1. A customer *sends a message*", "lead": "From your ad, your Instagram, or your website. Any time of day."},
            {"layout": "text", "headline": "2. The assistant *replies in seconds*", "lead": "It answers common questions and shares your designs and price ranges."},
            {"layout": "text", "headline": "3. It *qualifies the lead*", "lead": "Product, size, city, budget: the details your team needs to quote."},
            {"layout": "text", "headline": "4. It *sends the quote* and follows up", "lead": "A PDF quote on WhatsApp, then friendly reminders if they go quiet."},
            {"layout": "cta", "headline": "Your team *closes the deal.*", "lead": "Every lead and its status, in one dashboard."},
        ],
        "caption": "Here's exactly what happens when a customer messages a business that uses a WhatsApp lead assistant. Which step would save your team the most time?",
    },
    {
        "slides": [
            {"layout": "cover", "headline": "Is WhatsApp automation *right for you?*", "lead": "It's a great fit if you can say yes to these →"},
            {"layout": "list", "headline": "You're a good fit if…", "items": ["You get 10+ inquiries a day on WhatsApp or Instagram", "Each sale needs a quote or a conversation", "You run Facebook, Instagram or Google ads"]},
            {"layout": "list", "headline": "Especially if you sell…", "items": ["Furniture and interiors", "Kitchens and wardrobes", "Building materials or logistics services"]},
            {"layout": "cta", "headline": "Sound like you? *Let's talk.*", "lead": "Book a free 10-minute demo on WhatsApp."},
        ],
        "caption": "Not every business needs automation. Here's a quick way to tell if yours does.",
    },
    {
        "slides": [
            {"layout": "cover", "headline": "Myths about chatbots, *busted*", "lead": "Swipe →"},
            {"layout": "text", "headline": "\"It'll sound *robotic.*\"", "lead": "It's set up around your products, your questions and your tone, and it hands off to a person when needed."},
            {"layout": "text", "headline": "\"It's only for *big companies.*\"", "lead": "Small, owner-led businesses often benefit most. Every missed message is a missed sale."},
            {"layout": "text", "headline": "\"I'll lose control of *my chats.*\"", "lead": "You see every conversation in one dashboard, and your team can jump in anytime."},
            {"layout": "cta", "headline": "Still unsure? *See it live.*", "lead": "A free 10-minute demo, built around a business like yours."},
        ],
        "caption": "Three things people worry about before automating WhatsApp, and what actually happens.",
    },
    {
        "slides": [
            {"layout": "cover", "headline": "What happens to a lead *after 10 PM?*", "lead": "Two businesses, same message →"},
            {"layout": "text", "headline": "Business A: *no reply* until tomorrow", "lead": "The customer keeps searching and messages two competitors."},
            {"layout": "text", "headline": "Business B: *instant reply*", "lead": "Designs, price range and a question about size, within seconds."},
            {"layout": "text", "headline": "By morning, *B has the order.*", "lead": "Not because of price. Because of speed."},
            {"layout": "cta", "headline": "Be *Business B.*", "lead": "Let's set up your WhatsApp assistant."},
        ],
        "caption": "Same product, same price, same customer. The difference was who answered first.",
    },
    {
        "slides": [
            {"layout": "cover", "headline": "From 2 hours a day to *20 minutes*", "lead": "A real client story from Karachi →"},
            {"layout": "text", "headline": "The *problem*", "lead": "ALICO Enterprises' staff spent about 2 hours a day in Excel on quotes, invoices, stock and payments."},
            {"layout": "text", "headline": "The *solution*", "lead": "One business app for the full cycle: quote, challan, invoice, payment. It even works offline."},
            {"layout": "text", "headline": "The *result*", "lead": "Print-ready documents shared on WhatsApp, and the daily work done in about 20 minutes."},
            {"layout": "cta", "headline": "What could your team *stop doing by hand?*", "lead": "Tell us your process. We'll show you what to automate."},
        ],
        "caption": "How a Karachi general order supplier went from 2 hours of daily spreadsheet work to about 20 minutes.",
    },
    {
        "slides": [
            {"layout": "cover", "headline": "4 follow-up messages that *bring buyers back*", "lead": "Steal these →"},
            {"layout": "text", "headline": "Next day", "lead": "\"Hi! Just checking if you had any questions about the quote 😊\""},
            {"layout": "text", "headline": "Day 3", "lead": "\"We have a few new designs that might suit your space. Want to see them?\""},
            {"layout": "text", "headline": "Day 7", "lead": "\"Just a quick note: our current prices are valid until the end of the month.\""},
            {"layout": "text", "headline": "Day 14", "lead": "\"No pressure at all. Should I keep your quote on file for later?\""},
            {"layout": "cta", "headline": "Or let your assistant *send them for you.*", "lead": "Automatic, on time, every time."},
        ],
        "caption": "Most deals are won in the follow-up. Here are four messages you can start using today, or automate completely.",
    },
    {
        "slides": [
            {"layout": "cover", "headline": "What IMADI Tech *builds*", "lead": "Swipe to see what we can automate for you →"},
            {"layout": "list", "headline": "WhatsApp & Instagram", "items": ["AI assistants that reply instantly", "Quotes and catalogs on WhatsApp", "Automatic follow-ups"]},
            {"layout": "list", "headline": "Business systems", "items": ["Lead dashboards for your team", "ERP, invoicing and stock apps", "Custom SaaS products"]},
            {"layout": "cta", "headline": "Live for businesses in *Pakistan, the UK and Kenya.*", "lead": "Let's talk about yours."},
        ],
        "caption": "AI automation for businesses that sell through conversations. Here's what we build.",
    },
    {
        "slides": [
            {"layout": "cover", "headline": "Where do your leads *actually go?*", "lead": "A question every owner should ask →"},
            {"layout": "text", "headline": "They arrive on *many phones*", "lead": "Each salesperson has their own chats, and the owner sees none of them."},
            {"layout": "text", "headline": "Some get *forgotten*", "lead": "Others get answered late, and some quietly leave the company."},
            {"layout": "text", "headline": "One dashboard *changes that*", "lead": "Every lead, every conversation, every reply time, in one place."},
            {"layout": "cta", "headline": "See *every lead* you pay for.", "lead": "Ask us about lead tracking for your team."},
        ],
        "caption": "You pay for every lead your ads bring in. Can you see what happened to each one?",
    },
    {
        "slides": [
            {"layout": "cover", "headline": "Before you hire another *salesperson…*", "lead": "Read this →"},
            {"layout": "text", "headline": "Most of the work is *repetitive*", "lead": "Same questions, same price list, same follow-ups, every day."},
            {"layout": "text", "headline": "An assistant handles the *first steps*", "lead": "Instant replies, qualifying questions, quotes and reminders."},
            {"layout": "text", "headline": "Your team handles the *closing*", "lead": "They spend their time on buyers who are ready to decide."},
            {"layout": "cta", "headline": "Grow sales *without growing payroll.*", "lead": "Book a free 10-minute demo."},
        ],
        "caption": "Hiring is sometimes the answer. But often, the first step is taking the repetitive work off your team's plate.",
    },
]

REELS = [
    {
        "scenes": [
            {"headline": "You're paying for ads.", "sub": ""},
            {"headline": "*Who's answering* the messages?", "sub": ""},
            {"headline": "Late replies cost you *real customers.*", "sub": "They message three shops and buy from the first to answer."},
            {"headline": "An AI assistant replies *in seconds.*", "sub": "Day or night, on the WhatsApp number you already use."},
            {"headline": "Book a *free demo.*", "sub": "Chat with IMADI Tech on WhatsApp."},
        ],
        "voiceover": [
            "You're paying for ads.",
            "But who's answering the messages?",
            "Most customers message three businesses and buy from whoever replies first.",
            "An AI assistant answers every inquiry in seconds, day or night, on the WhatsApp number you already use.",
            "Book a free demo with IMADI Tech. The link is in our bio.",
        ],
        "caption": "You're paying for the clicks. Make sure someone's answering the messages.",
    },
    {
        "scenes": [
            {"headline": "What happens at *10:47 PM?*", "sub": "A customer asks for your price."},
            {"headline": "Without automation:", "sub": "No reply until tomorrow morning."},
            {"headline": "With automation:", "sub": "Instant reply, designs, price range and a quote."},
            {"headline": "By morning, *you have the lead.*", "sub": ""},
            {"headline": "Let's set yours up.", "sub": "IMADI Tech · WhatsApp automation"},
        ],
        "voiceover": [
            "It's ten forty-seven at night, and a customer asks for your price.",
            "Without automation, they wait until tomorrow.",
            "With automation, they get an instant reply, your designs, a price range, and a quote.",
            "By morning, the lead is yours.",
            "Want this for your business? Message IMADI Tech on WhatsApp.",
        ],
        "caption": "The same message at 10:47 PM. Two very different outcomes.",
    },
    {
        "scenes": [
            {"headline": "The sale happens *after the quote.*", "sub": ""},
            {"headline": "Buyers get *busy.*", "sub": "They compare, they forget, they go quiet."},
            {"headline": "A friendly follow-up *brings them back.*", "sub": ""},
            {"headline": "Your assistant sends it *automatically.*", "sub": "Next day, day three, day seven."},
            {"headline": "Never lose a quote *again.*", "sub": "Chat with us on WhatsApp."},
        ],
        "voiceover": [
            "Here's the truth: most sales happen after the quote.",
            "Buyers get busy. They compare, they forget, and they go quiet.",
            "A friendly follow-up is often all it takes to bring them back.",
            "Your WhatsApp assistant sends those follow-ups automatically, right on time.",
            "Never lose a quote again. Chat with IMADI Tech on WhatsApp.",
        ],
        "caption": "Quiet doesn't mean not interested. It usually means busy.",
    },
    {
        "scenes": [
            {"headline": "2 hours a day in *Excel.*", "sub": "Quotes, invoices, stock, payments."},
            {"headline": "That was ALICO Enterprises.", "sub": "A general order supplier in Karachi."},
            {"headline": "We built *one app* for all of it.", "sub": "It even works offline."},
            {"headline": "Now it takes *about 20 minutes.*", "sub": ""},
            {"headline": "What could *you* automate?", "sub": "IMADI Tech · imadi.tech"},
        ],
        "voiceover": [
            "Two hours every day, in Excel. Quotes, invoices, stock, and payments.",
            "That was ALICO Enterprises, a general order supplier in Karachi.",
            "We built them one app that handles all of it, and it even works offline.",
            "Now the same work takes about twenty minutes.",
            "What could your team stop doing by hand? Let's find out.",
        ],
        "caption": "A real client story: from 2 hours of daily spreadsheet work to about 20 minutes.",
    },
    {
        "scenes": [
            {"headline": "Customers message *three shops.*", "sub": ""},
            {"headline": "They buy from *the first to reply.*", "sub": ""},
            {"headline": "Not the cheapest.", "sub": "The fastest helpful answer."},
            {"headline": "Be first, *every time.*", "sub": "With a WhatsApp assistant."},
            {"headline": "Free 10-minute *demo.*", "sub": "Message IMADI Tech on WhatsApp."},
        ],
        "voiceover": [
            "Here's how people shop now. They message three businesses at once.",
            "And they usually buy from the first one to reply.",
            "Not the cheapest. The fastest helpful answer.",
            "With a WhatsApp assistant, you can be first every single time.",
            "Book a free ten-minute demo with IMADI Tech.",
        ],
        "caption": "Speed is the easiest competitive edge you'll ever get.",
    },
    {
        "scenes": [
            {"headline": "Where do your *leads go?*", "sub": ""},
            {"headline": "Different phones. *Different salespeople.*", "sub": ""},
            {"headline": "Some answered late. *Some never.*", "sub": ""},
            {"headline": "One dashboard. *Every lead.*", "sub": "Every chat, every reply time."},
            {"headline": "See what you're *paying for.*", "sub": "IMADI Tech · imadi.tech"},
        ],
        "voiceover": [
            "Do you know where your leads actually go?",
            "They land on different phones, with different salespeople.",
            "Some get answered late, and some never get answered at all.",
            "With one dashboard, you see every lead, every chat, and every reply time.",
            "See exactly what your ad budget is buying. Talk to IMADI Tech.",
        ],
        "caption": "You pay for every lead. You should be able to see every lead.",
    },
    {
        "scenes": [
            {"headline": "\"Chatbots sound *robotic.*\"", "sub": ""},
            {"headline": "Not when they're *built right.*", "sub": ""},
            {"headline": "Your products. Your questions. *Your tone.*", "sub": ""},
            {"headline": "And a *real person* when it matters.", "sub": "Serious buyers go straight to your team."},
            {"headline": "Hear it for *yourself.*", "sub": "Book a free demo on WhatsApp."},
        ],
        "voiceover": [
            "People tell us chatbots sound robotic.",
            "Not when they're built the right way.",
            "Your assistant knows your products, your common questions, and your tone.",
            "And when a customer is ready to buy, it hands them straight to a real person on your team.",
            "Hear it for yourself. Book a free demo on WhatsApp.",
        ],
        "caption": "A good assistant doesn't replace your team. It gets them better conversations.",
    },
    {
        "scenes": [
            {"headline": "No app to download.", "sub": ""},
            {"headline": "*Just WhatsApp.*", "sub": ""},
            {"headline": "Bookings, quotes, updates, *all in chat.*", "sub": ""},
            {"headline": "Your team sees it *on a dashboard.*", "sub": ""},
            {"headline": "Your customers are *already there.*", "sub": "IMADI Tech · WhatsApp automation"},
        ],
        "voiceover": [
            "No app to download. No forms to fill.",
            "Just WhatsApp.",
            "Your customers can book, get quotes, and receive updates, all inside a chat.",
            "And your team sees every request on one simple dashboard.",
            "Your customers are already on WhatsApp. Let's meet them there.",
        ],
        "caption": "The best customer experience is the one that happens where your customers already are.",
    },
    {
        "scenes": [
            {"headline": "Before you hire *another salesperson…*", "sub": ""},
            {"headline": "Most of the work is *repetitive.*", "sub": "Same questions. Same price list."},
            {"headline": "Let an assistant take the *first steps.*", "sub": "Replies, quotes, reminders."},
            {"headline": "Your team does the *closing.*", "sub": ""},
            {"headline": "Grow sales, *not payroll.*", "sub": "Message IMADI Tech on WhatsApp."},
        ],
        "voiceover": [
            "Before you hire another salesperson, think about this.",
            "Most of the daily work is repetitive. The same questions, and the same price list.",
            "An assistant can handle the first steps: replies, quotes, and reminders.",
            "So your team can focus on closing deals.",
            "Grow your sales, not your payroll. Message IMADI Tech on WhatsApp.",
        ],
        "caption": "Take the repetitive work off your team's plate first. Then decide if you need to hire.",
    },
    {
        "scenes": [
            {"headline": "Meet *IMADI Tech.*", "sub": "AI automation from Karachi."},
            {"headline": "WhatsApp & Instagram *assistants.*", "sub": ""},
            {"headline": "Lead dashboards and *business apps.*", "sub": ""},
            {"headline": "Live in *Pakistan, the UK and Kenya.*", "sub": ""},
            {"headline": "Let's build *yours.*", "sub": "Chat with us on WhatsApp."},
        ],
        "voiceover": [
            "Meet IMADI Tech, an AI automation company from Karachi.",
            "We build WhatsApp and Instagram assistants that reply instantly.",
            "Along with lead dashboards and business apps for growing teams.",
            "Our systems are live for businesses in Pakistan, the UK, and Kenya.",
            "Let's build yours. Chat with us on WhatsApp.",
        ],
        "caption": "AI automation for businesses that sell through conversations.",
    },
]

BANK = {"post": POSTS, "carousel": CAROUSELS, "reel": REELS}


def pick(fmt: str, nth: int) -> dict:
    items = BANK[fmt]
    return items[nth % len(items)]


# ------------------------------------------------------------- DEMO REELS --
# Real client work: screen recordings from assets/demos (shown with sample data).
# Every second reel slot uses one of these (client work and own products). `narration` plays over the video;
# `cta` plays over the closing scene.
DEMOS = [
    {
        "video": "alico-demo.mp4", "client": "Client work · ALICO Enterprises, Karachi",
        "headline": "One app runs the *whole business*",
        "points": ["Quotes, challans, invoices and payments", "Stock and ledgers in one place", "Works offline, shares to WhatsApp"],
        "narration": ["This is a real system we built for ALICO Enterprises in Karachi.",
                      "Quotations, challans, invoices, stock, and payments, all in one app.",
                      "It even works offline, and shares documents straight to WhatsApp.",
                      "Work that used to take two hours a day now takes about twenty minutes."],
        "cta": {"headline": "Want one for *your business?*", "line": "Want something like this for your business? Message IMADI Tech on WhatsApp."},
        "caption": ("Real client work: ALICO Business Suite.\n\nA general order supplier in Karachi was running quotations, challans, invoices, stock and payments across spreadsheets. We built one app for the whole cycle. It works offline and shares print-ready documents on WhatsApp.\n\nDaily paperwork went from about 2 hours to about 20 minutes. (Demo shown with sample data.)"),
    },
    {
        "video": "claims-bot.mp4", "client": "Client work · Logistics company, UK",
        "headline": "Damage claims, *filed on WhatsApp*",
        "points": ["Customer picks a claim type", "Sends details, photos and invoice", "Claim lands on the dashboard"],
        "narration": ["Here's a WhatsApp bot we built for a logistics company in the UK.",
                      "Customers file a damage claim right inside WhatsApp.",
                      "They send the details, labeled photos, and the invoice, step by step.",
                      "When they submit, the claim lands straight on the team's dashboard."],
        "cta": {"headline": "What could *your* bot handle?", "line": "What could a WhatsApp bot handle for your business? Let's talk."},
        "caption": ("Real client work: a WhatsApp claims bot for a UK logistics company.\n\nInstead of digging through emails, customers now file damage claims in a guided WhatsApp chat: details, labeled photos and the invoice PDF, all in one place. The team reviews everything on a dashboard. (Demo shown with sample data.)"),
    },
    {
        "video": "cm-demo.mp4", "client": "Client work · Multi-branch business, Nairobi",
        "headline": "See *every lead* across every branch",
        "points": ["Each branch links WhatsApp by QR", "Every conversation saved", "Diverted leads flagged for management"],
        "narration": ["This is Company Monitor, built for a multi-branch business in Nairobi.",
                      "Each branch links its WhatsApp Business number with a simple QR code.",
                      "Every lead and every conversation is saved in one dashboard.",
                      "So management can see when a lead is sent to a salesperson's personal number."],
        "cta": {"headline": "Know where *your leads go.*", "line": "Want to see where every one of your leads goes? Message IMADI Tech."},
        "caption": ("Real client work: Company Monitor.\n\nA multi-branch business in Nairobi needed to know what was happening to its WhatsApp leads. Each branch now links its WhatsApp Business number by QR code, every conversation is saved, and management can spot leads being diverted to personal numbers. (Demo shown with sample data.)"),
    },
    {
        "video": "renaz-bot.mp4", "client": "Client work · ReNaz, Karachi",
        "headline": "Book a pickup *in a WhatsApp chat*",
        "points": ["Choose scrap type and quantity", "Share location and a time slot", "Request goes to the dashboard"],
        "narration": ["Meet ReNaz, a scrap collection service in Karachi.",
                      "Customers book a pickup entirely inside WhatsApp.",
                      "They choose the type of scrap, share their location, and pick a time slot.",
                      "The request goes straight to the team's dashboard. No app to download."],
        "cta": {"headline": "Your customers are *already on WhatsApp.*", "line": "Your customers are already on WhatsApp. Let's build your bot."},
        "caption": ("Real client work: ReNaz WhatsApp booking bot.\n\nCustomers book scrap pickups in a simple WhatsApp conversation: scrap type, quantity, location and time slot. No app, no forms. Every request reaches the operations dashboard automatically. (Demo shown with sample data.)"),
    },
    {
        "video": "erp-demo.mp4", "client": "Client work · Logistics company, UK",
        "headline": "Invoices with *VAT, done for you*",
        "points": ["UK VAT applied automatically", "Credit notes in one click", "Email invoices from the app"],
        "narration": ["This is a custom accounting platform we built for a logistics company in the UK.",
                      "New invoices apply UK VAT automatically.",
                      "Credit notes take one click, and every report stays in sync.",
                      "Built around the way the team actually works."],
        "cta": {"headline": "Software built *around your process.*", "line": "Need software built around the way your team works? Talk to IMADI Tech."},
        "caption": ("Real client work: a custom ERP and accounting platform for a UK logistics company.\n\nThey were moving from manual accounting and wanted software built around their own process. Invoices apply UK VAT automatically, credit notes take one click, and invoices can be emailed straight from the app. (Demo shown with sample data.)"),
    },
    {
        "video": "renaz-dashboard.mp4", "client": "Client work · ReNaz, Karachi",
        "headline": "Every booking, *on one dashboard*",
        "points": ["Live operations overview", "New requests appear automatically", "Assign a verified collector"],
        "narration": ["Here's the other side of the ReNaz WhatsApp bot.",
                      "Every pickup a customer books on WhatsApp appears here automatically.",
                      "The team sees live operations at a glance.",
                      "And assigns each job to a verified collector in one click."],
        "cta": {"headline": "Chat in front. *Dashboard behind.*", "line": "Want a WhatsApp bot with a dashboard like this? Message IMADI Tech."},
        "caption": ("Real client work: the ReNaz operations dashboard.\n\nEvery pickup booked through the ReNaz WhatsApp bot appears here automatically. The team tracks requests, collectors and completed pickups, and assigns each job to a verified collector. (Demo shown with sample data.)"),
    },
    {
        "video": "claims-dashboard.mp4", "client": "Client work · Logistics company, UK",
        "headline": "Every claim, *in one place*",
        "points": ["Photos, PDF and details together", "Raise claims with the carrier", "Approve or reject in a click"],
        "narration": ["Behind the WhatsApp claims bot, there's a dashboard for the team.",
                      "Each claim arrives with its photos, invoice, and details in one place.",
                      "Staff can raise it with the carrier in a few clicks.",
                      "Then approve or reject it, and the customer is kept in the loop."],
        "cta": {"headline": "Stop digging *through emails.*", "line": "Ready to stop digging through emails? Message IMADI Tech on WhatsApp."},
        "caption": ("Real client work: the claims dashboard behind our UK logistics WhatsApp bot.\n\nEvery claim arrives complete, with photos, the invoice PDF and all details, so staff can raise, approve or reject it in a few clicks. (Demo shown with sample data.)"),
    },
]


# IMADI Tech's own products, built in-house.
PRODUCT_DEMOS = [
    {
        "video": "sales-engine-demo.mp4", "tag": "Built by IMADI Tech", "client": "IMADI AI Sales Engine",
        "headline": "AI finds leads. *You approve every email.*",
        "points": ["Finds and scores matching companies", "AI drafts a personal email for each lead", "Nothing is sent until a person approves"],
        "narration": ["This is the IMADI AI Sales Engine, built in-house at IMADI Tech.",
                      "You describe your ideal customer once, and it finds and scores matching companies.",
                      "For each lead, AI drafts a personalized email and explains its reasoning.",
                      "Nothing goes out until a person approves it. You stay in control."],
        "cta": {"headline": "Want a smarter *sales pipeline?*", "line": "Want AI to help fill your sales pipeline? Message IMADI Tech on WhatsApp."},
        "caption": ("Built by IMADI Tech: the AI Sales Engine.\n\nDescribe your ideal customer once. The engine finds matching companies, researches and scores each lead, and drafts a personalized outreach email with its reasoning. Nothing is sent until a person approves it, and every reply, meeting and deal is tracked in one pipeline. (Demo shown with sample data.)"),
    },
    {
        "video": "hercommerce-seller.mp4", "tag": "Built by IMADI Tech", "client": "HerCommerce · for women entrepreneurs",
        "headline": "An online store *in four steps*",
        "points": ["Pick what you sell", "Add products with photos and prices", "Get your own store link"],
        "narration": ["Meet HerCommerce, a platform we built for women who sell online.",
                      "A seller picks what she sells, and sets up her business in four simple steps.",
                      "She adds products with photos and prices.",
                      "Then she adds her WhatsApp number and gets her own store link."],
        "cta": {"headline": "Have a product idea? *Let's build it.*", "line": "Have an idea for a platform like this? Let's build it together."},
        "caption": ("Built by IMADI Tech: HerCommerce.\n\nMany women already sell through WhatsApp but can't set up or afford an online store. HerCommerce lets them create a store in four guided steps, add products with photos and prices, and share their own store link, with orders coming straight to WhatsApp. (Demo shown with sample data.)"),
    },
    {
        "video": "hercommerce-customer.mp4", "tag": "Built by IMADI Tech", "client": "HerCommerce · customer side",
        "headline": "Shop the store, *order on WhatsApp*",
        "points": ["Browse the seller's shop", "Add to cart, no account needed", "Order arrives on WhatsApp"],
        "narration": ["Here's HerCommerce from the customer's side.",
                      "Shoppers open the seller's store and browse her products.",
                      "They add items to the cart, with no account needed.",
                      "And the order arrives on the seller's WhatsApp, ready to confirm."],
        "cta": {"headline": "Sell where your customers *already chat.*", "line": "Want your customers to order straight on WhatsApp? Message IMADI Tech."},
        "caption": ("Built by IMADI Tech: the HerCommerce shopping experience.\n\nCustomers browse a seller's store, add products to the cart without creating an account, and place the order. It lands on the seller's WhatsApp, ready to confirm. Simple for shoppers, simple for sellers. (Demo shown with sample data.)"),
    },
]

# Client work and own products, mixed so the feed alternates between them.
DEMOS = [DEMOS[0], DEMOS[1], PRODUCT_DEMOS[0], DEMOS[2], DEMOS[3], PRODUCT_DEMOS[1],
         DEMOS[4], DEMOS[5], DEMOS[6], PRODUCT_DEMOS[2]]


def pick_reel(nth: int) -> tuple[str, dict]:
    """Reel slots alternate: talking reel, client demo, talking reel, client demo..."""
    if nth % 2 == 1 and DEMOS:
        return "demo", DEMOS[(nth // 2) % len(DEMOS)]
    return "talk", REELS[(nth // 2) % len(REELS)]
