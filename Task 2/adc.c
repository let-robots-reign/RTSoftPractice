#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/init.h>
#include <linux/fs.h>
#include <linux/cdev.h>
#include <stdbool.h>

#define DEVICE_NAME "ADC Imitation"

MODULE_AUTHOR("Zotov Alexey");
MODULE_DESCRIPTION("ADC Imitation");
MODULE_VERSION("1.0.0");
MODULE_LICENSE("GPL");

static int32_t major;
static int32_t counter = 0;
static bool is_open = false;

static struct file_operations fops = {
    .open = device_open,
    .close = device_close,
    .read = device_read
};

static int device_open(struct inode *, struct file *);

static ssize_t device_read(struct file *, char *, size_t, loff_t *);

static int device_release(struct inode *, struct file *);


int init_module(void) {
    printk(KERN_INFO "ADC loaded\n");

    major = register_chrdev(0, DEVICE_NAME, &fops);
    if (major < 0) {
        printk(KERN_ERR "Cannot initialize ADC module: %d\n", major);
        return major;
    }

    printk(KERN_INFO "Major is: %d", major);

    return 0;
}

void cleanup_module(void) {
    if (is_open) {
        printk(KERN_ALERT "Cannot stop ADC module because it is opened\n");
        return;
    }
    unregister_chrdev(major, DEVICE_NAME);
    printk(KERN_INFO "ADC module was cleaned up\n");
}

static int device_open(struct inode *inode, struct file *file) {
    if (is_open) {
        return -EBUSY;
    }
    is_open = true;
    return 0;
}

static ssize_t device_read(struct file *filp, char *buffer, size_t length, loff_t *offset) {
    size_t read = sprintf(buffer, "%d\n", counter++);
    return read;
}

static int device_release(struct inode *inode, struct file *file) {
    is_open = false;
    return 0;
}
