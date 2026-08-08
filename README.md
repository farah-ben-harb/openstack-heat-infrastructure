# OpenStack Heat Infrastructure Deployment

Infrastructure-as-code deployment for OpenStack using a Heat template (HOT).

## Overview

This project provisions a complete cloud environment including:

- Multi-network architecture for frontend and backend traffic
- Router and network interfaces
- Security groups
- Virtual machines with Ubuntu and CirrOS
- Block storage through Cinder volumes
- Floating IPs for external access

The goal is to show reproducible cloud infrastructure definition using native OpenStack tooling.

## Architecture

- 2 networks:
  - Frontend network `10.10.0.0/24`
  - Backend network `10.20.0.0/24`
- 1 router connecting both networks to the external network
- 4 instances:
  - 2 Ubuntu instances
  - 2 CirrOS instances
- Security groups controlling access by role
- Cinder volumes attached where persistent storage is needed

## Repository Structure

- `template.txt` Heat template source
- `.gitattributes` repository metadata

## Usage

- Review the Heat template before deployment
- Validate the parameters for your OpenStack environment
- Launch the stack from Horizon or the OpenStack CLI
- Verify networking, floating IPs, and instance readiness after deployment

## Branching and Commits

- Use branches such as `feat/<area>`, `fix/<area>`, `docs/<area>`, or `infra/<area>`
- Keep commits focused on one infrastructure concern
- Prefer Conventional Commits such as `feat(openstack): add backend security group`
- Avoid vague commit messages like `update`, `final`, or `test`

## Contributing

- Keep environment-specific values out of the template where possible
- Document any change that affects the network or security model
- Avoid committing generated state or credentials

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
