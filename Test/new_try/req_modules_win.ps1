# Install required Python modules
$modules = @('psutil', 'pyyaml', 'gputil', 'pymongo', 'pandas', 'scikit-learn')

foreach ($module in $modules) {
    try {
        pip install $module
        Write-Host "Successfully installed $module"
    } catch {
        Write-Host "Failed to install $module. Please check the installation manually."
    }
}
