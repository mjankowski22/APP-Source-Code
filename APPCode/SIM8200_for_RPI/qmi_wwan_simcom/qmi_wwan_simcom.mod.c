#include <linux/module.h>
#define INCLUDE_VERMAGIC
#include <linux/build-salt.h>
#include <linux/vermagic.h>
#include <linux/compiler.h>

BUILD_SALT;

MODULE_INFO(vermagic, VERMAGIC_STRING);
MODULE_INFO(name, KBUILD_MODNAME);

__visible struct module __this_module
__section(".gnu.linkonce.this_module") = {
	.name = KBUILD_MODNAME,
	.init = init_module,
#ifdef CONFIG_MODULE_UNLOAD
	.exit = cleanup_module,
#endif
	.arch = MODULE_ARCH_INIT,
};

#ifdef CONFIG_RETPOLINE
MODULE_INFO(retpoline, "Y");
#endif

static const struct modversion_info ____versions[]
__used __section("__versions") = {
	{ 0x4766f3ab, "module_layout" },
	{ 0xbc5c03ec, "usbnet_disconnect" },
	{ 0xe92a07fa, "usbnet_tx_timeout" },
	{ 0x9d664533, "usbnet_change_mtu" },
	{ 0xc456140b, "eth_validate_addr" },
	{ 0xc8525cef, "usbnet_start_xmit" },
	{ 0x29f48bdd, "usbnet_stop" },
	{ 0xd4b24cfa, "usbnet_open" },
	{ 0xe6bd5aaa, "usb_deregister" },
	{ 0xb1b79332, "usb_register_driver" },
	{ 0x184ae64b, "skb_push" },
	{ 0xdfc1185f, "__dev_kfree_skb_any" },
	{ 0x83e548a4, "skb_pull" },
	{ 0x3da8b2df, "usbnet_probe" },
	{ 0x5c215af7, "usbnet_suspend" },
	{ 0x7df72f89, "usbnet_resume" },
	{ 0x8db178de, "usbnet_get_ethernet_addr" },
	{ 0x79aa04a2, "get_random_bytes" },
	{ 0x56755c4a, "_dev_err" },
	{ 0x7977a84a, "usb_control_msg" },
	{ 0xffeaebe8, "_dev_info" },
	{ 0xe2fae0eb, "usb_cdc_wdm_register" },
	{ 0x91eb0f9b, "usbnet_get_endpoints" },
	{ 0x29a5ad56, "usb_driver_claim_interface" },
	{ 0x8198cbc4, "usb_ifnum_to_if" },
	{ 0xb8e33064, "eth_commit_mac_addr_change" },
	{ 0xfe53a6e7, "eth_prepare_mac_addr_change" },
	{ 0x96d18f99, "usb_driver_release_interface" },
	{ 0xb57fd9d2, "usb_autopm_put_interface" },
	{ 0x437d1d51, "usb_autopm_get_interface" },
	{ 0xb1ad28e0, "__gnu_mcount_nc" },
};

MODULE_INFO(depends, "cdc-wdm");

MODULE_ALIAS("usb:v1E0Ep9001d*dc*dsc*dp*ic*isc*ip*in05*");

MODULE_INFO(srcversion, "29480A58515EB2DB048A6C6");
