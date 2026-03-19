# OpenStack Heat Infrastructure Deployment

## Project Overview
This project provides an automated infrastructure deployment on **OpenStack** using a **Heat template (HOT)**.

It provisions a complete cloud environment including:
- Multi-network architecture (frontend & backend)
- Router and network interfaces
- Security groups
- Virtual machines (Ubuntu & CirrOS)
- Block storage (Cinder volumes)
- Floating IPs for external access

The infrastructure is fully reproducible and designed for cloud and DevOps environments.

---

## Architecture Overview
The deployed infrastructure includes:

- 2 Networks:
  - Frontend Network (10.10.0.0/24)
  - Backend Network (10.20.0.0/24)

- 1 Router:
  - Connects both networks to external network

- 4 Instances:
  - 2 Ubuntu instances (frontend & backend)
  - 2 CirrOS instances (frontend & backend)

- 2 Cinder Volumes:
  - 10GB each
  - Attached to Ubuntu instances only

- 4 Floating IPs:
  - One for each instance

- Security Group:
  - Allows SSH (22), HTTP (80), HTTPS (443), MySQL (3306), ICMP

---

## Features
- Full infrastructure provisioning using **Heat (IaC)**
- Multi-tier network architecture (frontend/backend)
- Automated VM deployment (Ubuntu & CirrOS)
- Persistent storage with Cinder volumes
- External access via floating IPs
- Secure access configuration (SSH, Web, DB)
- Cloud-init configuration for Ubuntu instances

---

## Technologies Used
- **OpenStack** – Cloud infrastructure  
- **Heat (HOT)** – Infrastructure as Code  
- **Neutron** – Networking  
- **Nova** – Compute instances  
- **Cinder** – Block storage  
- **Cloud-init** – Instance initialization  

---

## Template Parameters
The template allows customization via parameters:

- `external_network` – Public network (default: provider)
- `ubuntu_image` – Ubuntu image name
- `cirros_image` – CirrOS image name
- `ubuntu_flavor` – Flavor for Ubuntu instances
- `cirros_flavor` – Flavor for CirrOS instances
- `key_name` – SSH key pair

---

## Deployment

### 1. Upload Template
```bash
openstack stack create \
  -t template.yaml \
  my-stack
