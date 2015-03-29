## Install

Follow the generic plugin installation instructions in [the FIR wiki](https://github.com/certsocietegenerale/FIR/wiki/Plugins).
Make sure the following line is included in the `urlpatterns` variable in `fir/urls.py`:

```
url(r'^articles/', include('fir_articles.urls', namespace='articles')),
```

## Usage

This plugin adds a new entry in the main navbar named `Árticles`.
