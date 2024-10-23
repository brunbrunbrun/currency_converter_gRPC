# REQUIREMENTS

```bash
pip install -r requirements.txt
```

# USAGE

- On a computer run `server.py`.
- On another computer in the same network, setup `client.py` by pointing to the server's IP address with `grpc.insecure_channel('192.168.x.x:port')` by default the application uses the `50051` port.
- After setup, run the `client.py` script.

# TROUBLESHOOTING

Verify if the specified port is open, on Unix you can run:
```bash
sudo ufw allow 50051/tcp
```
to allow connections to a specified port, in this case, port `50051`.

# ACKNOWLEGDES

This project utilizes the [ExchangeRate-API](https://www.exchangerate-api.com/) for updated ratios.
