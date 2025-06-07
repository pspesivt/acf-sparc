# CI/CD Pipeline Templates

## Release Pipeline (.github/workflows/release.yml)

```yaml
name: Create and Publish Release
on:
  workflow_dispatch:
    inputs:
      version_type:
        description: 'Semantic version type (major, minor, patch)'
        required: true
        type: choice
        options: [patch, minor, major]
jobs:
  release:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      packages: write
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - id: versioning
        run: |
          npm install -g standard-version
          standard-version --release-as ${{ inputs.version_type }}
          VERSION=$(jq -r .version package.json)
          echo "version=${VERSION}" >> $GITHUB_OUTPUT
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - run: |
          IMAGE_ID=ghcr.io/${{ github.repository }}
          IMAGE_TAG=${{ steps.versioning.outputs.version }}
          docker build . -t ${IMAGE_ID}:${IMAGE_TAG}
          docker push ${IMAGE_ID}:${IMAGE_TAG}
      - run: |
          git push
          git push --tags
      - uses: benc-uk/workflow-dispatch@v1
        with:
          workflow: deploy.yml
          token: ${{ secrets.PAT_TOKEN }}
          inputs: '{ "version": "${{ steps.versioning.outputs.version }}", "environment": "staging" }'
```

## Deployment Pipeline (.github/workflows/deploy.yml)

```yaml
name: Deploy Release
on:
  workflow_dispatch:
    inputs:
      version:
        description: 'The exact version tag to deploy (e.g., v1.2.3)'
        required: true
      environment:
        description: 'Target environment'
        required: true
        type: choice
        options: [staging, production]
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    steps:
      - uses: appleboy/ssh-action@v1.0.0
        with:
          host: ${{ secrets.DEPLOY_HOST }}
          username: deploy
          key: ${{ secrets.DEPLOY_KEY }}
          script: |
            IMAGE="ghcr.io/${{ github.repository }}:${{ inputs.version }}"
            /opt/scripts/deploy-app.sh $IMAGE
```