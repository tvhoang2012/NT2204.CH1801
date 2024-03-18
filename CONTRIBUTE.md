# How to contribute

1. Fork the project
2. Checkout with new branch
    ```
    git checkout -b feature/AmazingFeature
    ```
3. Code ding and test your feature. Go to the report directory and build the report with your environment or docker exist. Check report pdf file generate after build process.
    ```
    docker-compose up --build
    ```
    in window
    ```
    docker compose up --build
    ```
4. Add and commit your change
```
git add .
git commit -m 'Add some AmazingFeature'
```
5. Push your change to fork repository
```
git push --set-upstream origin feature/AmazingFeature
```
6. Go to [pull request](https://github.com/sonnh-uit/NT2204.CH1801/pulls) and create pull request to master branch.