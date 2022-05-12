all: build push

B=$(shell git symbolic-ref HEAD | sed -e "s,.*/\(.*\),\1,")
build : app
	docker build --platform linux/x86_64 \
	-t middleware_cotools_linux_server:${B} .

push:

	docker tag middleware_cotools_linux_server:$(B) registry.gitlab.si.francetelecom.fr/lrousselotdesaintceran/co-tools-api-middleware:$(B)
	docker push registry.gitlab.si.francetelecom.fr/lrousselotdesaintceran/co-tools-api-middleware:$(B)




run_brmc:
	docker run \
	--env HTTP_PROXY="http://fpc.itn.intraorange:8080" \
	--env HTTPS_PROXY="http://fpc.itn.intraorange:8080" \
	--env NO_PROXY="gitlab.si.francetelecom.fr" \
	-p 8095:80 \

	registry.gitlab.si.francetelecom.fr/lrousselotdesaintceran/co-tools-api-middleware

run_local:
	docker run \
	-p 8000:80 \
	-v $(PWD)/app/cert/:/code/app/cert/ \
	registry.gitlab.si.francetelecom.fr/lrousselotdesaintceran/co-tools-api-middleware

clean:
	yes | docker container prune
	yes | docker image prune
