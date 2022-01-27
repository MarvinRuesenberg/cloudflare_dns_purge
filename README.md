# Cloudflare DNS Purge

After switching from my current DNS Nameserver to Cloudflare, Cloudflare offered the option to dynamically import the already existing DNS-Records for a smooth transition.

Unfortunately, that lead to 200+ DNS-Records when i originally had about 6.

I assume this had to do with a wildcard record on my old provider.

Anyways...If you, like me, do not want to delete alot of DNS Records by hand, feel free to give this script a try.

### Requirements

The script needs your API-Token for Cloudflare. If you dont have one already go to

"Profile -> API Tokens -> Create Token"

Make sure you create the Token for the appropriate Zone and check that you set **Edit** permissions for it.

### Usage

Insert your **API-Token** into the appropriate variable:

``
token = "<API-TOKEN>"
``

The script will then run you through the process via User-Input.

**Before** deleting anything, it fetches the current BIND-Config from Cloudflare so in case you accidentally delete too much, you can restore it by importing it in Cloudflare itself.

### Post Scriptum

The script was written fairly quickly, so please feel free to improve/adapt it to your needs or raise a pull-request.
As i am fairly new to Github please be patient as it might take me some time to get used to the workflow.
