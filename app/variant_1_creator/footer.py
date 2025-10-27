import random

RESPONSIBLE_USE_PRINCIPLES = [
    "Be Kind & Inclusive – Treat all users with empathy and respect. Welcome diverse perspectives and avoid content or behavior that excludes or demeans people based on identity or background.",
    "Prioritize Safety of Minors – Do not share or request sexual, exploitative, or age-inappropriate content. Report any suspected exploitation or grooming immediately.",
    "Report Problems & Feedback – If you encounter harmful content, security issues, or bugs, report them promptly so they can be addressed.",
    "Accessibility & Usability – Create content and interactions that are accessible to all users, including those using assistive technologies.",
    "No Malware or Harmful Tools – Do not share or distribute malware, hacking tools, or anything designed to damage or disrupt systems.",
    "Respect Others – Avoid offensive, abusive, or discriminatory behavior. No harassment, hate speech, or threats.",
    "Use Fairly – Do not exploit or misuse app features, automate interactions unfairly, or manipulate data or results.",
    "Protect Privacy – Never share personal or sensitive information publicly or without consent.",
    "Stay Safe – Be mindful of your digital wellbeing. Take breaks and use the app in moderation.",
    "Legal Compliance – Follow all local laws and regulations. Unlawful use of the app is strictly prohibited.",
    "Content Responsibility – You are responsible for the content you create, share, or upload. Ensure it is accurate, lawful, and respectful of others’ rights.",
    "Honest Interaction – Be truthful in how you represent yourself. Avoid fake identities, impersonation, or deceptive practices."
]

GAME_TERMS = [
    "Fair Play: Play honestly and avoid cheating, exploiting bugs, or using unauthorized software or automation.",
    "Respect Others: Treat all players with kindness. No harassment, hate speech, or offensive behavior.",
    "Account Responsibility: Keep your login details secure. You’re responsible for activity on your account.",
    "Content Ownership: Game assets, artwork, and code belong to the developers. Don’t copy, modify, or redistribute them without permission.",
    "Privacy: We collect minimal data needed to improve gameplay. Your information will not be shared without consent.",
    "Updates & Changes: Game features, balance, or rules may change as we improve the experience.",
    "Legal Use: Use the game only in compliance with local laws and app store policies."
]

GAME_FAQ = [
    "Is the game free to play? Yes! The core game is free to play. Optional in-app purchases are available for cosmetic items or faster progress.",
    "Can I recover my account if I lose access? Yes, link your account to an email or social login to enable recovery.",
    "How do I protect my account? Don’t share your login info and make sure to link your account to your email or social profile for recovery.",
    "Can I change my username? Yes, you can update your profile name in the settings menu. Keep it appropriate and respectful.",
    "How quickly will my issue be resolved? Response times may vary, but the support team will assist as soon as possible.",
    "How do I contact support? Visit the Help & Support section",
    "Are there community rules I should follow? Yes, be respectful and follow the code of conduct to maintain a safe environment.",
    "Are my personal details shared with other players? No, sensitive information is kept private and secure."
]


def get_use_principles():
    """Return a random selection of principles"""
    selected = [p for p in RESPONSIBLE_USE_PRINCIPLES if random.choice([True, False])]
    if not selected:
        selected.append(random.choice(RESPONSIBLE_USE_PRINCIPLES))
    return "<br>".join(selected)

def get_terms():
    """Return a random selection of terms"""
    selected = [p for p in GAME_TERMS if random.choice([True, False])]
    if not selected:
        selected.append(random.choice(GAME_TERMS))
    return "<br>".join(selected)

def get_faq():
    """Return a random selection of faq"""
    selected = [p for p in GAME_FAQ if random.choice([True, False])]
    if not selected:
        selected.append(random.choice(GAME_FAQ))
    return "<br>".join(selected)