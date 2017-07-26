# Runs the most current stable [Interactive Brokers Gateway](https://www.interactivebrokers.com/en/index.php?f=16457) installer and allows to configure the Gateway settings before committing the configured container.  
## Steps to install and use IB Gateway:
1. Run the container using either: `docker run -e VNC_PASSWORD=your-password -p 5900:5900 sebfia/ib-gateway-stable` or `docker-compose build`
2. Wait for IB Gateway to start and enter your login credentials
3. Adapt the API settings to your needs.
4. Close IB Gateway which will stop the container and commit the container's state to a new image: `docker commit <your-container-name> <your-locally-configured-image-name>`
5. Use your configured image for further processing
