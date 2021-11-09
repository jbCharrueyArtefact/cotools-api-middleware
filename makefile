all: build push

build : app
	docker build --platform linux/x86_64 \
	--build-arg USER_EMAIL="louis.rousselotdesaintceran.ext@orange.com" \
	--build-arg USER_NAME="Louis Rousselot" \
	 -t \
	middleware_cotools_linux_server:0.1.0 .

push: 
	docker tag middleware_cotools_linux_server:0.1.0 registry.gitlab.si.francetelecom.fr/lrousselotdesaintceran/co-tools-api-middleware
	docker push registry.gitlab.si.francetelecom.fr/lrousselotdesaintceran/co-tools-api-middleware




run_brmc:
	docker run \
	-v /home/osadmin/:/sa/ \
	--env GOOGLE_APPLICATION_CREDENTIALS=/sa/ofr-0tm-iam-secu-1-prd-a6536a6660b8.json \
	--env HTTP_PROXY="http://fpc.itn.intraorange:8080" \
	--env HTTPS_PROXY="http://fpc.itn.intraorange:8080" \
	--env NO_PROXY="gitlab.si.francetelecom.fr" \
	-p 8095:80 \
	
	registry.gitlab.si.francetelecom.fr/lrousselotdesaintceran/co-tools-api-middleware 

run_local: 
	docker run \
	-v ~/desktop/artefact/orange/co-tools-api-middleware/sa/:/sa/ \
	--env GOOGLE_APPLICATION_CREDENTIALS=/sa/ofr-0tm-iam-secu-1-prd-a6536a6660b8.json \
	-p 8000:80 \
	middleware_cotools_linux_server:0.1.0 

clean:
	yes | docker container prune
	yes | docker image prune

