# email-registration

## Deploy

```bash
sudo git clone  --no-checkout https://github.com/gqqnbig/email-registration.git shine-registration
sudo chown -R www-data: shine-registration
sudo chmod -R 775 shine-registration
cd shine-registration
git sparse-checkout init --cone
git sparse-checkout set src deploy
git remote set-branches origin 'master'
git fetch --all


# If the installation folder is on a mount point, the service file must be copied.
# systemd runs before mount points are loaded.
# see https://github.com/systemd/systemd/issues/8307
if [[ $(df --output=target /var/www/shine-registration/deploy/systemd/system/ | tail -n 1) == '/' ]]; then
	sudo ln -s /var/www/shine-registration/deploy/systemd/system/uwsgi-registration.service /etc/systemd/system/
else
	sudo cp /var/www/shine-registration/deploy/systemd/system/uwsgi-registration.service /etc/systemd/system/
fi
```
