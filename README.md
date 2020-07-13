# plivo-gotify-forwarder

Run this to forward incoming texts from Plivo to Gotify.

## Installation

- Install python and pipenv on a webserver.
  - If you're dealing with multiple python versions on this server, consider using pyenv to install python; it's minimal and lovely and plays nice with pipenv.
- Clone this directory somewhere on a server; maybe `/usr/local/share/plivo-gotify-forwarder`.
- Run `pipenv install`
- Change the secret key in `plivo-gotify-forwarder.py`
- Install the systemd service by copying `plivo-gotify-forwarder.service` from `systemd/` to `/etc/systemd/system/`.
- Reload systemd service definitions: `sudo systemd daemon-reload`
- Start the service now and at all future boots: `sudo systemctl enable --now plivo-gotify-forwarder`
- Set up a route in your webserver to serve requests using local port 1622 (see below)

## Usage

If you're running a gotify server at `https://push.example.com` using nginx, you can add this in the same server section as gotify to use plivo-gotify-forwarder to handle all routes beginning with `/plivo/`:

```nginx
    # turns POST /plivo/token into gotify mesage
	location /plivo/ {
		proxy_pass http://127.0.0.1:1622/;
		proxy_redirect     off;
		proxy_set_header   Host $host;
	}
```

Restart nginx with `sudo systemctl restart nginx`.

Next, create a gotify token for Plivo using the gotify web interface at `https://push.example.com`. I'll call this `THE_TOKEN` from now on.

Then, log into Plivo and create a new application to send POST requests to `https://push.example.com/plivo/THE_TOKEN`. Attach this application to some telephone number endpoint.

Now try hitting the example route at `https://push.example.com/plivo/test` with a GET request. This should return `OK`.

Finally, try hitting the example route with the following POST request (run in your terminal; curl must be installed):

```sh
    curl -X POST -d From=Alice To=Bob Text=attackatdawn https://push.example.com/plivo/THE_TOKEN.
```

You can now "receive texts" from the virtual number to a gotify application on your phone!

## Troubleshooting

- Is the systemd service already installed and running? Try `sudo systemctl status plivo-gotify-forwarder` or `sudo journalctl -ue plivo-gotify-forwarder`.
- Have you already changed the secret key from the default?
- Are the permissions already set on the cloned repository directory in such a way that systemd-configured user can see the files?
- Is your webserver (nginx or whatever) already configured properly?
- Is gotify accessible from the internet?
- Is the Plivo application set up / enabled / attached to a phone number? You can check the log and debug log sections for info on how far the message is getting.
