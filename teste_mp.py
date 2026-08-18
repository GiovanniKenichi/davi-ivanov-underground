import mercadopago

ACCESS_TOKEN = "APP_USR-2645220806235246-072818-0907fabc1d2cd9c0a2fc9a201c25ad56-3572996373"

sdk = mercadopago.SDK(ACCESS_TOKEN)

print(sdk.user().get())