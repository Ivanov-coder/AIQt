// 这部分暂时打算用于搭建 网络服务器
// 后面会使用Django框架

package main

import (
	"log"
	"github.com/gin-gonic/gin"	
)

func main() {
	router := gin.Default()
	router.GET("/", func(ctx *gin.Context){
		ctx.String(200, "Hello, World!")
	})
	router.Run(":9999")
	log.Println("Hello, World!")
}