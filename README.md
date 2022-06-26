# Charts Only Go Up

June 26, 2022: Repo made public.

Code for [ChartsOnlyGoUp.com](https://chartsonlygoup.com).

Note: Code is provided as is. It is likely not usable in its current state, for various reasons. That said, several fans have asked (after updates stopped Q1'2021), so here it is.

**Production - start server**

```
gunicorn --bind 0.0.0.0:5000 run:app

gunicorn -w 3 run:app

```

**Development - refresh app**

```
supervisorctl restart charts
```



# Screenshots

[Charts Only Go Up - home](https://chartsonlygoup.com)

![Charts Only Go Up - home](/screenshots/Charts Only Go Up - home.png)

[Charts Only Go Up - stock chart - AAPL](https://chartsonlygoup.com/aapl)

![Charts Only Go Up - chart - top - AAPL](/screenshots/Charts Only Go Up - chart - top - AAPL.png)

![Charts Only Go Up - chart - middle - AAPL](/screenshots/Charts Only Go Up - chart - middle - AAPL.png)

![Charts Only Go Up - chart - bottom - AAPL](/screenshots/Charts Only Go Up - chart - bottom - AAPL.png)

