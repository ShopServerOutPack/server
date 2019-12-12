

menu_top = [
    {
        "label": "首页",
        "path": "/wel/index",
        "icon": 'el-icon-document',
        "meta": {
            "i18n": 'dashboard',
        },
        "parentId": 0
    },
    {
        "label": "测试",
        "path": "/test/index",
        "icon": 'el-icon-document',
        "meta": {
            "i18n": 'test',
        },
        "parentId": 1
    },
]

first = [
    {
        "label": "人员管理",
        "path": '/personnelHandler',
        "meta": {
            "i18n": 'personnelHandler',
        },
        "icon": 'icon-caidan',
        "children": [
            {
                "label": "用户管理",
                "path": 'merchantManagement',
                "component": 'views/personnelHandler/merchantManagement',
                "meta": {
                    "i18n": 'merchantManagement',
                    "keepAlive": True
                },
                "icon": 'icon-caidan',
                "children": []
            }
        ],
    },
    {
        "label": "小程序管理",
        "path": '/wechatHandler',
        "meta": {
            "i18n": 'wechatHandler',
        },
        "icon": 'icon-caidan',
        "children": [
            # {
            #     "label": "公告管理",
            #     "path": 'memoHandler',
            #     "component": 'views/wechatHandler/memoHandler',
            #     "meta": {
            #         "i18n": 'memoHandler',
            #         "keepAlive": False
            #     },
            #     "icon": 'icon-caidan',
            #     "children": []
            # },
            # {
            #     "label": "联系我们管理",
            #     "path": 'lianxiwomenHandler',
            #     "component": 'views/wechatHandler/lianxiwomenHandler',
            #     "meta": {
            #         "i18n": 'lianxiwomenHandler',
            #         "keepAlive": False
            #     },
            #     "icon": 'icon-caidan',
            #     "children": []
            # },
            {
                "label": "轮播图",
                "path": 'bannerHandler',
                "component": 'views/wechatHandler/bannerHandler',
                "meta": {
                    "i18n": 'bannerHandler',
                    "keepAlive": False
                },
                "icon": 'icon-caidan',
                "children": []
            },
            {
                "label": "素材管理",
                "path": 'attachment',
                "component": 'views/wechatHandler/attachment',
                "meta": {
                    "i18n": 'attachment',
                    "keepAlive": False
                },
                "icon": 'icon-caidan',
                "children": []
            },
            {
                "label": "商品分类管理",
                "path": 'typeHandler',
                "component": 'views/wechatHandler/videoHandler/typeHandler',
                "meta": {
                    "i18n": 'typeHandler',
                    "keepAlive": True
                },
                "icon": 'icon-caidan',
                "children": []
            },
            {
                "label": "商品管理",
                "path": 'videoHandler',
                "component": 'views/wechatHandler/videoHandler/videoHandler',
                "meta": {
                    "i18n": 'videoHandler',
                    "keepAlive": True
                },
                "icon": 'icon-caidan',
                "children": []
            },
        ],
    },
    {
        "label": "系统管理",
        "path": '/systemManagement',
        "meta": {
            "i18n": 'systemManagement',
        },
        "icon": 'icon-caidan',
        "children": [
            {
                "label": "系统参数",
                "path": 'SysParams',
                "meta": {
                    "i18n": 'SysParams'
                },
                "icon": 'icon-caidan',
                "children": [
                    # {
                    #     "label": "支付方式",
                    #     "path": 'Paytype',
                    #     "component": 'views/systemManagement/Paytype',
                    #     "meta": {
                    #         "i18n": 'Paytype',
                    #         "keepAlive": True
                    #     },
                    #     "icon": 'icon-caidan',
                    #     "children": []
                    # },
                    # {
                    #     "label": "支付渠道",
                    #     "path": 'Paypass',
                    #     "component": 'views/systemManagement/Paypass',
                    #     "meta": {
                    #         "i18n": 'Paypass',
                    #         "keepAlive": True
                    #     },
                    #     "icon": 'icon-caidan',
                    #     "children": []
                    # }
                ]
            },
            {
                "label": "缓存管理",
                "path": 'Cache',
                "component": 'views/systemManagement/Cache',
                "meta": {
                    "i18n": 'Cache'
                },
                "icon": 'icon-caidan',
                "children": []
            },
        ]
    }
]


all_menu = {
    "top" : menu_top,
    "first" : first
}
