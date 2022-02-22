# ig2wp
Export Instagram Posts into WordPress Posts

# Requirements

- Have WordPress Administrator Prvileges
- Have Username/Password to Instagram Account

# Instructions

## Create a WordPress Application Password

1. Navigate to your blog's /wp-admin endpoint and on the left sidebar, select Users.
2. Select a user with media and posting privilieges. Your administrator user is fine.
3. Scroll to the bottom where it says "Application Passwords". Add a new application password. Give it whatever name you want. Hold onto these credentials.

## Install and run the Instaloader application

1. Visit the [Instaloader Github](https://github.com/instaloader/instaloader) for information on installation, configuration, and exececution. 
2. Upon running the application, you will have a directory containing files ending in `.json.xz`, `.jpg`, `.mp4`, and `.txt`. Make a note of this directory location. You will need it later.


## Install the IG2WP Application

Install the IG2WP python application from source. You may pip install directly from Github as shown below.

```
pip install git+https://github.com/aderbique/ig2wp.git
```

## Configure and Run the IG2WP Application

You have the option of specifying the parameters on each runtime, or by saving the contents to a configuration file. The `-w` parameter writes your variables to the config file for you.

```
$ ig2wp -s https://my-wordpress-blog.com -u <your wp username> -p '<the application password you generated>' -d </path/to/instaloader/account> -want
```

Example:

```
$ ig2wp -s https://blog.derbique.us -u austin -p '5EC5 PpLf 5rVn Ekwe 8JWE KWEP' -d '~/instaloader/austinadventure' -w
```

### Modifying the Configuration file

Simply edit the file after it's generated

```
vim ~/.ig2wp/config.ini
```

# Bug Reporting

Please submit bug reports through Github