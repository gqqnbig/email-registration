# email-registration

## Deploy

```
sudo git clone  --no-checkout https://github.com/gqqnbig/email-registration.git shine-registration
sudo chown -R www-data: shine-registration
sudo chmod -R 775 shine-registration
cd shine-registration
git sparse-checkout init --cone
git sparse-checkout set src deploy
git remote set-branches origin 'master'
git fetch --all

sudo ln -s /var/www/shine-registration/deploy/systemd/system/uwsgi-registration.service /etc/systemd/system/
```
