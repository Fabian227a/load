# Iciniga2 und load Skript

## Load Skript in Python
Siehe: custom_load

## Incinga 2 Installation
[Incinga2 Ubuntu Dokumentation](https://icinga.com/docs/icinga-web/latest/doc/02-Installation/02-Ubuntu/)

- Terminal öffnen und als sudo User anmelden

```
sudo -s
```

- Icinga Package Repository hinzufügen

```
apt update
apt -y install apt-transport-https wget gnupg

wget -O - https://packages.icinga.com/icinga.key | gpg --dearmor -o /usr/share/keyrings/icinga-archive-keyring.gpg

. /etc/os-release; if [ ! -z ${UBUNTU_CODENAME+x} ]; then DIST="${UBUNTU_CODENAME}"; else DIST="$(lsb_release -c| awk '{print $2}')"; fi; \
 echo "deb [signed-by=/usr/share/keyrings/icinga-archive-keyring.gpg] https://packages.icinga.com/ubuntu icinga-${DIST} main" > \
 /etc/apt/sources.list.d/${DIST}-icinga.list
 echo "deb-src [signed-by=/usr/share/keyrings/icinga-archive-keyring.gpg] https://packages.icinga.com/ubuntu icinga-${DIST} main" >> \
 /etc/apt/sources.list.d/${DIST}-icinga.list

apt update
```

- Incinga2 installieren

```
apt install icinga2 -y
```

- Icinga2 Konfiguration überprüfen

```
icinga2 daemon -C
```

## Datenbank (MariaDB) installieren
```
apt install mariadb-server -y
```

- MariaDB zum starten (bei Serverstart) hinzufügen und starten
```
systemctl enable mysql
systemctl start mysql
```

- Root-Passwort für Datenbank Administrator hinzufügen
```
mysql_secure_installation
```
- Enter current password für root: Da noch kein Passwort gesetzt ist mit "Enter" bestätigen
- Neues Passwort setzen: Y
- Passwort eingeben und bestätigen
- Alles andere mit "Enter" betätigen


## Icinga2 MySql IDO Tools installieren
- Damit kann Icinga2 mit der Datenbank kommunizieren
```
apt install icinga2-ido-mysql -y
```
- Alles mit "Ja" bestätigen und Passwort eingeben und bestätigen

- MySql IDO zu Icinga hinzufügen
```
icinga2 feature enable ido-mysql
```
- Iciniga2 neustarten
```
systemctl restart iciniga2
```

## IcingaWeb2 installieren und konfigurieren
- Apache und PHP installieren
```
apt install php
apt install imagemagick
apt install php-imagick
apt install apache2
```

- Installation Icingaweb2
```
apt install icingaweb2 icingacli libapache2-mod-php php-gd -y
```


(ggf. Vim Texteditor installieren)
```
apt install vim -y
```

(ggf. PHP Version prüfen)
```
ls /etc/php
```

- Zeitzone anpassen
```
vim /etc/php/<PHP-VERSION>/apache2/php.ini
```

- mit "/timezone" nach Zeile suchen
- mit "i" in insert modus wechseln
- Zeile anpassen: ';date.timezone =' =>  'date.timezone = "Europe/Berlin"'
- mit "esc" in den Befehlsmodus wechseln
- mit ":wq" Datei speichern und schließen


- Apache neustarten
```
systemctl restart apache2
```


## Icinga2 API
Kommunikation mit der Icinga2 API

- Setup laufen lassen (Zertifikate und Konfigurationsdateien erzeugen)
```
icinga2 api setup
```
- Api User bearbeiten
```
vim /etc/icinga2/conf.d/api-users.conf
```
- "root" Passwort ändern oder aufschreiben

- "Web user hinzufügen"
```
object ApiUser "icinga2" {
  password = "<Passwort eingeben>"
  permissions = [ "status/query", "actions/*", "objects/modify/*", "objects/query/*" ]
}
```

- Icinga2 neustarten
```
systemctl restart icinga2
```

## Einrichtung
- Browser öffnen und zu <http://localhost/icingaweb2> navigieren
- "Webbased Setup Wizard" auswählen

- Installationstoken erzeugen
```
icingacli setup config directory --group icingaweb2
```
```
icingacli setup token create
```

- Token kopieren und einfügen
- Für die restliche konfiguration siehe <http://https.readmailreallyfast.de/monitoring-host-mit-icinga2/icinga-web-2/> + lokale Anpassungen sofern notwendig


## Custom Load Skript als Plugin zu Icinga2 hinzufügen
- custom_load.py runterladen
- In das Verzeichnis der Datei navigieren
- umbennen:
```
mv custom_load.py custom_load
```

- Berechtigungen setzen
```
chmod +x custom_load
```

- Zum Testen ausführen
```
./custom_load
```

- custom_load in Icinga2 Plugin Verzeichnis kopieren
```
cp -u custom_load /usr/lib/nagios/plugins/custom_load
```

## Plugin und Service zu Icinga2 hinzufügen
- In das Icinga2 Konfigurations-Verzeichnis navigieren
```
cd /etc/icinga2/conf.d/
```

-- commands.conf Datei bearbeiten und einfügen

```
vim commands.conf
```

```
// In der Datei commands.conf

object CheckCommand "custom_load" {
  import "plugin-check-command"
  command = [ PluginDir + "/custom_load" ]

  arguments = {
    "--interval" = {
      value = 10
      description = "Check interval in seconds"
    }
  }

  timeout = 30s
}
```

- hosts.conf prüfen (sowas in der Art steht da drin)
```
// In der Datei hosts.conf

object Host "mein_server" {
  import "generic-host"
  address = "192.168.1.1"
  vars.os = "linux" // oder passende Variable für dein Betriebssystem
}

```

- Service konfigurieren
```
vim services.conf
```

```
// In der Datei services.conf

apply Service "custom_load" {
  import "generic-service"
  check_command = "custom_load"
  assign where host.vars.os == "linux"
}

```

- Generiche Host Konfiguration
```
vim generic-host.conf
```

```
// In der Datei generic-host.conf

template Host "generic-host" {
  max_check_attempts = 3
  check_interval = 1m
  retry_interval = 30s
  // Weitere generische Host-Einstellungen
}

```

- Generiche Services Konfiguration
```
vim generic-service.conf
```

```
// In der Datei generic-service.conf

template Service "generic-service" {
    max_check_attempts = 3
    check_interval = 1m
    retry_interval = 30s
    // Weitere generische Service-Einstellungen
}


```

- Icinga2 Konfiguration prüfen
```
sudo icinga2 daemon -C
```

- Incing2 neustarten
```
sudo systemctl restart icinga2
```