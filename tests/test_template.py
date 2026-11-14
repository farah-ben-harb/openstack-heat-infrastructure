from pathlib import Path

import yaml


TEMPLATE_PATH = Path(__file__).parents[1] / "template.txt"


def load_template() -> dict:
    with TEMPLATE_PATH.open(encoding="utf-8") as template_file:
        return yaml.safe_load(template_file)


def test_template_has_expected_heat_structure() -> None:
    template = load_template()

    assert str(template["heat_template_version"]) == "2018-08-31"
    assert {"parameters", "resources", "outputs"} <= template.keys()
    assert "admin_cidr" in template["parameters"]
    assert "default" not in template["parameters"]["admin_cidr"]


def test_security_group_restricts_administration_and_keeps_mysql_private() -> None:
    security_group = load_template()["resources"]["sg_all"]["properties"]
    rules = security_group["rules"]

    ssh_rules = [rule for rule in rules if rule.get("port_range_min") == 22]
    icmp_rules = [rule for rule in rules if rule.get("protocol") == "icmp"]
    assert ssh_rules == [
        {
            "protocol": "tcp",
            "direction": "ingress",
            "port_range_min": 22,
            "port_range_max": 22,
            "remote_ip_prefix": {"get_param": "admin_cidr"},
        }
    ]
    assert icmp_rules == [
        {
            "protocol": "icmp",
            "direction": "ingress",
            "remote_ip_prefix": {"get_param": "admin_cidr"},
        }
    ]
    assert not any(
        rule.get("port_range_min") == 3306 or rule.get("port_range_max") == 3306
        for rule in rules
    )


def test_network_resources_have_explicit_router_dependencies() -> None:
    resources = load_template()["resources"]

    for name, router_interface in (
        ("frontend_subnet", "router_int_frontend"),
        ("backend_subnet", "router_int_backend"),
    ):
        assert name in resources
        assert router_interface in resources

    for name in ("port_u1", "port_u2", "port_c1", "port_c2"):
        assert resources[name]["depends_on"].startswith("router_int_")

    for name in ("fip_u1", "fip_u2", "fip_c1", "fip_c2"):
        assert resources[name]["depends_on"].startswith("router_int_")


def test_servers_use_key_authentication_and_no_plaintext_passwords() -> None:
    resources = load_template()["resources"]

    for name in ("ubuntu1", "ubuntu2", "cirros1", "cirros2"):
        server = resources[name]["properties"]
        assert server["key_name"] == {"get_param": "key_name"}
        assert "password" not in server

    cloud_config = resources["cloud_config"]["properties"]["cloud_config"]
    assert cloud_config["ssh_pwauth"] is False
    assert cloud_config["users"][0]["lock_passwd"] is True
