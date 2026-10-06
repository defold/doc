---
title: Defold development for Microsoft Xbox
brief: This manual describes how to get access to Defold's Xbox support and development tools
---

# Game development for Microsoft Xbox consoles

To develop Xbox console games with Defold, you need to be an approved Xbox developer and have access to Defold's Xbox support and Microsoft's console development tools.

## Registering as an Xbox developer

Start at Microsoft's [Xbox publishing page](https://developer.microsoft.com/en-US/games/publish) to learn about its publishing programs, including ID@Xbox, and follow the registration and approval process for Xbox console development.

Access to Microsoft's secure Xbox resources requires your organization to be onboarded as an Xbox development partner and to have a valid Microsoft Game Development Kit (GDK) agreement.

## Xbox access in Defold

Once Microsoft has approved you for Xbox console development, [contact Defold](https://defold.com/contact/) to request access to Defold's Xbox support and arrange confirmation of your developer status.

Once your status has been confirmed, we will provide access to Xbox-specific Defold resources and instructions for getting started, including:

- The Xbox extension with platform-specific API integrations for user management and game saves.
- Instructions for building, bundling and testing Xbox games with Defold.
- Xbox-specific support through the [Defold Xbox development forum](https://forum.defold.com/c/for-xbox-development-discussions).

Console development details covered by Microsoft's NDA are provided through authorized documentation and support channels.

## Downloading GXDK

The Gaming eXtensions Development Kit (GXDK) contains Xbox console development tools and is distributed with the Microsoft Game Development Kit with Xbox Extensions (GDKX). The [public GDK](https://github.com/microsoft/GDK) download does not include the Xbox console tools.

1. Use your organization's Microsoft Entra ID account associated with its Microsoft Partner Center account.
2. Ask your Microsoft representative to enable access to Secure Xbox Downloads. Download access is not managed through Partner Center.
3. Open [Secure Xbox Downloads](https://aka.ms/gdkdl) and sign in with that account. If access is missing, use **Switch directory** to select your organization's directory.
4. Download the GDKX release required by your Defold Xbox setup and follow the included installation instructions on your Windows development PC.

See Microsoft's [GDK resource access guide](https://learn.microsoft.com/en-us/gaming/gdk/docs/gdk-dev/development-downloads/access-resources) for account setup and access troubleshooting.

## Support

- Use the [Defold Xbox development forum](https://forum.defold.com/c/for-xbox-development-discussions) for Defold-specific Xbox questions.
- Use the [Xbox Live developer forums](https://forums.xboxlive.com/) for Microsoft Xbox development support. Access requires an authorized Xbox developer account.

## FAQ

#### Q: Do I need to install additional tools to develop for Xbox?

A: Yes. Install the GDK with Xbox Extensions (GDKX) on your Windows development PC. Follow the setup instructions supplied with your Defold Xbox access for the required SDK version and the steps for building and testing your game.

#### Q: Can I use a single code base for Xbox and other platforms?

A: You can share game logic and assets across supported Defold platforms. Xbox-specific integrations, such as user management and game saves, use the Xbox extension and may require platform-specific code.
