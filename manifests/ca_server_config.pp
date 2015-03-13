node default {
    include 'python'

    python::requirements { '/vagrant/requirements.txt':
    }
}
