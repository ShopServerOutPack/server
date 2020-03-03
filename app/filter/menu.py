

menu_top = [
    {
        "label": "首页",
        "path": "/dashboard",
        "icon": 'el-icon-s-home',
        "meta": {
            "i18n": 'dashboard',
        },
        "parentId": 0
    }
]

first = [
    {
        "label": "用户管理",
        "path": '/merchantManagement',
        "component": 'views/personnelHandler/index',
        "meta": {
            "i18n": 'merchantManagement',
            "keepAlive": True
        },
        "icon": 'el-icon-user-solid',
        "children": []
    },
    {
        "label": "订单管理",
        "path": '/order',
        "component": 'views/wechatHandler/order',
        "meta": {
            "i18n": 'order',
            "keepAlive": False
        },
        "icon": 'el-icon-s-order',
        "children": []
    },
    {
        "label": "素材管理",
        "path": '/attachment',
        "component": 'views/wechatHandler/attachment',
        "meta": {
            "i18n": 'attachment',
            "keepAlive": False
        },
        "icon": 'el-icon-picture',
        "children": []
    },
    {
        "label": "轮播图管理",
        "path": '/bannerHandler',
        "component": 'views/wechatHandler/bannerHandler',
        "meta": {
            "i18n": 'bannerHandler',
            "keepAlive": False
        },
        "icon": 'el-icon-picture-outline-round',
        "children": []
    },
    {
        "label": "商品管理",
        "path": '/goods',
        "component": 'views/wechatHandler/goods',
        "meta": {
            "i18n": 'goods',
            "keepAlive": True
        },
        "icon": 'el-icon-s-goods',
        "children": []
    },
    {
        "label": "分类管理",
        "path": '/category',
        "component": 'views/wechatHandler/category',
        "meta": {
            "i18n": 'category',
            "keepAlive": True
        },
        "icon": 'el-icon-menu',
        "children": []
    },
    {
        "label": "热门分类管理",
        "path": '/hotcategory',
        "component": 'views/wechatHandler/hotcategory',
        "meta": {
            "i18n": 'hotcategory',
            "keepAlive": True
        },
        "icon": 'el-icon-menu',
        "children": []
    },
    {
        "label": "推荐分类管理",
        "path": '/tjcategory',
        "component": 'views/wechatHandler/tjcategory',
        "meta": {
            "i18n": 'tjcategory',
            "keepAlive": True
        },
        "icon": 'el-icon-menu',
        "children": []
    },
    {
        "label": "充值卡管理",
        "path": '/czcard',
        "component": 'views/wechatHandler/czcard',
        "meta": {
            "i18n": 'czcard',
            "keepAlive": True
        },
        "icon": 'el-icon-bank-card',
        "children": []
    },
    # {
    #     "label": "虚拟商品卡密管理",
    #     "path": '/yhcard',
    #     "component": 'views/wechatHandler/yhcard',
    #     "meta": {
    #         "i18n": 'yhcard',
    #         "keepAlive": True
    #     },
    #     "icon": 'el-icon-bank-card',
    #     "children": []
    # },
    # {
    #     "label": "小程序管理",
    #     "path": '/wechatHandler',
    #     "meta": {
    #         "i18n": 'wechatHandler',
    #     },
    #     "icon": 'icon-caidan',
    #     "children": [
    #         {
    #             "label": "轮播图",
    #             "path": 'bannerHandler',
    #             "component": 'views/wechatHandler/bannerHandler',
    #             "meta": {
    #                 "i18n": 'bannerHandler',
    #                 "keepAlive": False
    #             },
    #             "icon": 'icon-caidan',
    #             "children": []
    #         },
    #         {
    #             "label": "商品分类管理",
    #             "path": 'typeHandler',
    #             "component": 'views/wechatHandler/videoHandler/typeHandler',
    #             "meta": {
    #                 "i18n": 'typeHandler',
    #                 "keepAlive": True
    #             },
    #             "icon": 'icon-caidan',
    #             "children": []
    #         },
    #         {
    #             "label": "商品管理",
    #             "path": 'videoHandler',
    #             "component": 'views/wechatHandler/videoHandler/videoHandler',
    #             "meta": {
    #                 "i18n": 'videoHandler',
    #                 "keepAlive": True
    #             },
    #             "icon": 'icon-caidan',
    #             "children": []
    #         },
    #     ],
    # },
    {
        "label": "系统管理",
        "path": '/systemManagement',
        "meta": {
            "i18n": 'systemManagement',
        },
        "icon": 'el-icon-setting',
        "children": [
            {
                "label": "缓存管理",
                "path": 'Cache',
                "component": 'views/systemManagement/Cache',
                "meta": {
                    "i18n": 'Cache'
                },
                "icon": 'el-icon-setting',
                "children": []
            },
            {
                "label": "系统参数",
                "path": 'Sysparams',
                "component": 'views/systemManagement/sysparams',
                "meta": {
                    "i18n": 'sysparams'
                },
                "icon": 'el-icon-setting',
                "children": []
            },
            {
                "label": "角色维护",
                "path": 'Role',
                "component": 'views/systemManagement/role',
                "meta": {
                    "i18n": 'role'
                },
                "icon": 'el-icon-setting',
                "children": []
            },
        ]
    }
]


all_menu = {
    "top" : menu_top,
    "first" : first
}
