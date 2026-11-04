
def generate_safety_response(
    reason: str,
    language: str
) -> str:

    responses = {
        "en": (
            "Your safety is important. Based on what you "
            "described, there may be a safety concern.\n\n"
            "Please stop using the appliance if it is safe "
            "to do so. Do not touch or unplug it if there "
            "is smoke, fire, or an electrical hazard. Move "
            "away if there is immediate danger and contact "
            "local emergency services.\n\n"
            "Do not attempt to open or repair the appliance. "
            "Please contact Géant customer support for assistance."
        ),

        "fr": (
            "Votre sécurité est importante. D'après votre "
            "description, il pourrait y avoir un risque.\n\n"
            "Veuillez cesser d'utiliser l'appareil si vous "
            "pouvez le faire sans danger. Ne le touchez pas "
            "et ne le débranchez pas en présence de fumée, "
            "de flammes ou d'un danger électrique. Éloignez-vous "
            "en cas de danger immédiat et contactez les services "
            "d'urgence locaux.\n\n"
            "N'essayez pas d'ouvrir ou de réparer l'appareil. "
            "Veuillez contacter le service client Géant."
        ),

        "ar": (
            "سلامتك مهمة بالنسبة لنا. بناءً على وصفك، "
            "قد تكون هناك مشكلة تتعلق بالسلامة.\n\n"
            "يرجى التوقف عن استخدام الجهاز إذا كان ذلك "
            "آمنًا. لا تلمس الجهاز ولا تفصله عن الكهرباء "
            "إذا كان هناك دخان أو حريق أو خطر كهربائي. "
            "ابتعد عن المكان عند وجود خطر مباشر واتصل "
            "بخدمات الطوارئ المحلية.\n\n"
            "لا تحاول فتح الجهاز أو إصلاحه. يرجى التواصل "
            "مع خدمة عملاء Géant للحصول على المساعدة."
        )
    }

    return responses.get(language, responses["en"])
